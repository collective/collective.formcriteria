import urllib

from zope.component import getMultiAdapter
from zope.i18n import translate

from Acquisition import aq_inner
from Missing import MV
from DateTime.interfaces import IDateTime

from Products.Five.browser import metaconfigure
from Products.Five.browser import pagetemplatefile

from Products.CMFCore.utils import getToolByName
from Products.CMFCore import Expression

from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone import PloneBatch
from plone.memoize import view

from plone.app.content.browser import tableview
from plone.app.content.browser import foldercontents


class Table(metaconfigure.ViewMixinForTemplates, tableview.Table):
    """Use a table template which obeys the columns fields"""

    index = pagetemplatefile.ViewPageTemplateFile("table.pt")

    def render(self, *args, **kw):
        """Delegate to the registered template"""
        return self.index(*args, **kw)

    def update(self, base_url, view_url, items, batch, columns,
               show_sort_column=False, buttons=[], pagesize=20):
        self._batch = batch
        context = aq_inner(self.context)
        tableview.Table.__init__(
            self, request=self.request, base_url=base_url,
            view_url=view_url, items=items,
            show_sort_column=show_sort_column, buttons=buttons,
            pagesize=batch.size)
        map(self.set_checked, items)
        self.__dict__['context'] = context
        self.columns = columns

    @property
    @view.memoize
    def batch(self):
        """Use the collection batch"""
        return self._batch

    @property
    def islastpage(self):
        return self.batch.numpages == self.batch.pagenumber

    @property
    def items_on_page(self):
        if self.islastpage:
            remainder = self.batch.sequence_length % self.batch.size
            if remainder == 0:
                return self.batch.size
            else:
                return remainder
        else:
            return self.batch.size

    @property
    def items_not_on_page(self):
        items_on_page = list(self.items)
        return [item for item in self.items if item not in
                items_on_page]

    @apply
    def selectcurrentbatch():
        def set(self, value):
            self._selectcurrentbatch = value
            if self._selectcurrentbatch and self.show_all or (
                self.batch.sequence_length <= self.pagesize):
                self.selectall = True
        return property(
            tableview.Table._get_select_currentbatch, set)

    @property
    def within_batch_size(self):
        return self.batch.sequence_length < self.pagesize


class FolderContentsTable(foldercontents.FolderContentsTable):
    """Use a table template which obeys the columns fields"""

    # Used for evaluating TALES
    index = pagetemplatefile.ViewPageTemplateFile('empty.pt')

    # Copied from
    # plone.app.content.browser.foldercontents.FolderContentsTable
    # v1.2.5
    def __init__(self, context, request, contentFilter={}):
        """Use a table template which obeys the columns fields"""
        self.context = context
        self.request = request
        self.contentFilter = request

        sort_info = context.restrictedTraverse(
            '@@sort_info').getSortInfo()
        self.columns = context.restrictedTraverse('columns_view')

        # If a sort has been selected by the user, make sure it will
        # be picked up by the topic.  This is done by adding it to the
        # request.
        sort_on = contentFilter.get('sort_on')
        if sort_on in sort_info['sorts']:
            sort = self.columns.sorts[sort_on]
            request[sort] = True

        url = context.absolute_url()
        view_url = url + '/@@folder_contents'
        self.table = context.restrictedTraverse(
            '@@folder_contents_table')
        self.table.update(url, view_url, self.items, self.batch,
            self.columns, show_sort_column=self.show_sort_column,
            buttons=self.buttons)

    @property
    @view.memoize
    def batch(self):
        """Let the collection batch the results"""
        context = aq_inner(self.context)
        if self.request.get('show_all', '').lower() == 'true':
            results = context.queryCatalog(
                self.contentFilter, batch=False)
            return PloneBatch.Batch(
                results, len(results),
                int(self.request.get('b_start', 0)), orphan=0)
        return context.queryCatalog(self.contentFilter, batch=True)

    @property
    @view.memoize
    def items(self):
        """Use the item brains"""
        # Mostly copied from plone.app.content.browser.foldercontents,
        # modified to use catalog brains
        context = aq_inner(self.context)
        plone_utils = getToolByName(context, 'plone_utils')
        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        portal_workflow = getToolByName(context, 'portal_workflow')
        portal_properties = getToolByName(context, 'portal_properties')
        portal_types = getToolByName(context, 'portal_types')
        site_properties = portal_properties.site_properties
        portal = getToolByName(context, 'portal_url').getPortalObject()

        use_view_action = site_properties.getProperty(
            'typesUseViewActionInListings', ())
        browser_default = context.browserDefault()

        econtext = Expression.getExprContext(context)

        results = []
        for i, obj in enumerate(self.batch):
            if (i + 1) % 2 == 0:
                table_row_class = "draggable even"
            else:
                table_row_class = "draggable odd"

            url = obj.getURL()
            path = obj.getPath or "/".join(obj.getPhysicalPath())
            icon = plone_view.getIcon(obj)

            type_class = 'contenttype-' + plone_utils.normalizeString(
                obj.portal_type)

            review_state = obj.review_state
            state_class = 'state-' + plone_utils.normalizeString(review_state)
            relative_url = obj.getURL(relative=True)

            type_title_msgid = portal_types[obj.portal_type].Title()
            url_href_title = u'%s: %s' % (translate(type_title_msgid,
                                                    context=self.request),
                                          safe_unicode(obj.Description))

            modified = plone_view.toLocalizedTime(
                obj.ModificationDate, long_format=1)

            obj_type = obj.Type
            if obj_type in use_view_action:
                view_url = url + '/view'
            elif obj.is_folderish:
                view_url = url + "/folder_contents"
            else:
                view_url = url

            is_browser_default = len(browser_default[1]) == 1 and (
                obj.id == browser_default[1][0])

            columns = {}
            for column in self.columns.ordered:
                value = getattr(obj, column['field'], MV)

                # Calculate the sums before using any expression
                if value is not MV:
                    if column['has_sum']:
                        if 'sum' in column:
                            column['sum'] += value
                        else:
                            column['sum'] = value

                expr = column.get('expr')
                if expr:
                    econtext.vars.update(item=obj, value=value)
                    value = econtext.evaluate(expr)
                    del econtext.vars['value']
                    del econtext.vars['item']

                if IDateTime.providedBy(value):
                    value = plone_view.toLocalizedTime(value, long_format=1)

                columns[column['field']] = value

            results.append(dict(
                url=url,
                url_href_title=url_href_title,
                id=obj.getId,
                quoted_id=urllib.quote_plus(obj.getId),
                path=path,
                title_or_id=obj.pretty_title_or_id(),
                obj_type=obj_type,
                size=obj.getObjSize,
                modified=modified,
                icon=icon.html_tag(),
                type_class=type_class,
                wf_state=review_state,
                state_title=portal_workflow.getTitleForStateOnType(
                    review_state, obj_type),
                state_class=state_class,
                is_browser_default=is_browser_default,
                folderish=obj.is_folderish,
                relative_url=relative_url,
                view_url=view_url,
                table_row_class=table_row_class,
                is_expired=context.isExpired(obj),
                obj=obj,
                columns=columns,
                ))

        for column in self.columns.ordered:
            if not column['has_sum'] or 'sum' not in column:
                continue
            expr = column.get('expr')
            if expr:
                econtext.vars.update(item=obj, value=column['sum'])
                column['sum'] = econtext.evaluate(expr)
                del econtext.vars['value']
                del econtext.vars['item']

        return results

    @property
    def buttons(self):
        buttons = []
        context = aq_inner(self.context)
        portal_actions = getToolByName(context, 'portal_actions')
        button_actions = portal_actions.listActionInfos(
            object=context, categories=('folder_topic_buttons', ))

        # Do not show buttons if there is no data, unless there is data to be
        # pasted
        if not len(self.items):
            if self.context.cb_dataValid():
                for button in button_actions:
                    if button['id'] == 'paste':
                        return [self.setbuttonclass(button)]
            else:
                return []

        for button in button_actions:
            # Make proper classes for our buttons
            if button['id'] != 'paste' or context.cb_dataValid():
                buttons.append(self.setbuttonclass(button))
        return buttons


class FolderContentsMixin(object):

    def __call__(self, *args, **kw):
        context = aq_inner(self.context)
        self.columns = context.restrictedTraverse('columns_view')
        return super(FolderContentsMixin, self).__call__(*args, **kw)


class FolderContentsView(FolderContentsMixin,
                         foldercontents.FolderContentsView):
    """List items in a tabular form including object buttons"""

    def __init__(self, context, request):
        # Bypass the interface request declaration that blocks the
        # workflow menu
        super(foldercontents.FolderContentsView, self).__init__(
            context, request)

    def contents_table(self):
        """Use the request as the contentFilter"""
        table = FolderContentsTable(self.context, self.request)
        return table.render()


if hasattr(foldercontents, 'FolderContentsKSSView'):
    # BBB Plone 4.2
    FolderContentsBrowserView = foldercontents.FolderContentsKSSView
else:
    FolderContentsBrowserView = foldercontents.FolderContentsBrowserView


class FolderContentsKSSView(FolderContentsMixin, FolderContentsBrowserView):
    table = FolderContentsTable
