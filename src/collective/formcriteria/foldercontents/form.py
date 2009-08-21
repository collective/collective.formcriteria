import urllib

from zope.component import getMultiAdapter
from zope.app import pagetemplate
from zope.i18n import translate

import Acquisition

from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.utils import safe_unicode
from plone.memoize import instance

from plone.app.content.browser import tableview
from plone.app.content.browser import foldercontents

class Table(tableview.Table):
    """Use a table template which obeys the columns fields"""                

    render = pagetemplate.ViewPageTemplateFile("table.pt")

    def __init__(self, context, request, base_url, view_url, items,
                 batch, columns, show_sort_column=False, buttons=[],
                 pagesize=20):
        map(self.set_checked, items)
        super(Table, self).__init__(
            request=request, base_url=base_url, view_url=view_url,
            items=items, show_sort_column=show_sort_column,
            buttons=buttons, pagesize=pagesize)
        self.context = context
        self.columns = columns
        self._batch = batch

    @property
    @instance.memoize
    def batch(self):
        """Use the collection batch"""
        return self._batch

class FolderContentsTable(foldercontents.FolderContentsTable):
    """Use a table template which obeys the columns fields"""                

    # Copied from
    # plone.app.content.browser.foldercontents.FolderContentsTable
    # v1.2.5
    def __init__(self, context, request, contentFilter={}):
        """Use a table template which obeys the columns fields"""
        self.context = context
        self.request = request
        self.contentFilter = contentFilter

        column_vocab = context.Vocabulary('customViewFields')[0]
        link_columns = context.getField(
            'customViewLinks').getAccessor(context)()
        columns = [
            dict(id=column, name=column_vocab.getValue(column),
                 link=(column in link_columns))
            for column in context.getCustomViewFields()]

        url = context.absolute_url()
        view_url = url + '/@@folder_contents'
        self.table = Table(
            context, request, url, view_url, self.items, self.batch,
            columns, show_sort_column=self.show_sort_column,
            buttons=self.buttons)

    @property
    @instance.memoize
    def batch(self):
        """Let the collection batch the results"""
        context = Acquisition.aq_inner(self.context)
        return context.queryCatalog(self.contentFilter, batch=True)

    @property
    @instance.memoize
    def items(self):
        """Use the item brains"""
        context = Acquisition.aq_inner(self.context)
        plone_utils = getToolByName(context, 'plone_utils')
        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        portal_workflow = getToolByName(context, 'portal_workflow')
        portal_properties = getToolByName(context, 'portal_properties')
        portal_types = getToolByName(context, 'portal_types')
        site_properties = portal_properties.site_properties
        
        use_view_action = site_properties.getProperty('typesUseViewActionInListings', ())
        browser_default = context.browserDefault()

        results = []
        for i, obj in enumerate(self.batch):
            if (i + 1) % 2 == 0:
                table_row_class = "draggable even"
            else:
                table_row_class = "draggable odd"

            url = obj.getURL()
            path = obj.getPath or "/".join(obj.getPhysicalPath())
            icon = plone_view.getIcon(obj);
            
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
                                 
            results.append(dict(
                url = url,
                url_href_title = url_href_title,
                id  = obj.getId,
                quoted_id = urllib.quote_plus(obj.getId),
                path = path,
                title_or_id = obj.pretty_title_or_id(),
                obj_type = obj_type,
                size = obj.getObjSize,
                modified = modified,
                icon = icon.html_tag(),
                type_class = type_class,
                wf_state = review_state,
                state_title = portal_workflow.getTitleForStateOnType(review_state,
                                                           obj_type),
                state_class = state_class,
                is_browser_default = is_browser_default,
                folderish = obj.is_folderish,
                relative_url = relative_url,
                view_url = view_url,
                table_row_class = table_row_class,
                is_expired = context.isExpired(obj),
                obj=obj,
            ))
        return results

    @property
    def buttons(self):
        buttons = []
        context = Acquisition.aq_inner(self.context)
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
    
class FolderContentsView(foldercontents.FolderContentsView):
    """List items in a tabular form including object buttons"""
    
    def contents_table(self):
        """Use the request as the contentFilter"""
        table = FolderContentsTable(
            self.context, self.request, contentFilter=self.request)
        return table.render()
