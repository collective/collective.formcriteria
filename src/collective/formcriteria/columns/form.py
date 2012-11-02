import urllib

from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.i18n import translate

from plone.memoize import instance

from Acquisition import aq_inner, aq_base

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.CMFPlone.utils import pretty_title_or_id

try:
    from Products.CMFPlone.utils import isExpired
    isExpired  # pyflakes
except ImportError:

    from DateTime import DateTime
    from Products.CMFPlone.utils import base_hasattr
    from Products.CMFPlone.utils import safe_callable

    # BBB
    def isExpired(content):
        """ Find out if the object is expired (copied from skin script) """

        expiry = None

        # NOTE: We also accept catalog brains as 'content' so that the
        # catalog-based folder_contents will work. It's a little
        # magic, but it works.

        # ExpirationDate should have an ISO date string, which we need to
        # convert to a DateTime

        # Try DC accessor first
        if base_hasattr(content, 'ExpirationDate'):
            expiry = content.ExpirationDate

        # Try the direct way
        if not expiry and base_hasattr(content, 'expires'):
            expiry = content.expires

        # See if we have a callable
        if safe_callable(expiry):
            expiry = expiry()

        # Convert to DateTime if necessary, ExpirationDate may return 'None'
        if expiry and expiry != 'None' and isinstance(expiry, basestring):
            expiry = DateTime(expiry)

        if isinstance(expiry, DateTime) and expiry.isPast():
            return 1
        return 0

from plone.app.content.browser import foldercontents


class FolderContentsTable(foldercontents.FolderContentsTable):
    """Use non-catalog folder contents for the column UI"""

    def folderitems(self):
        """
        """
        context = aq_inner(self.context)
        plone_utils = getToolByName(context, 'plone_utils')
        plone_view = getMultiAdapter((context, self.request), name=u'plone')
        plone_layout = queryMultiAdapter(
            (context, self.request), name=u'plone_layout',
            default=plone_view)
        portal_workflow = getToolByName(context, 'portal_workflow')
        portal_properties = getToolByName(context, 'portal_properties')
        portal_types = getToolByName(context, 'portal_types')
        site_properties = portal_properties.site_properties

        use_view_action = site_properties.getProperty(
            'typesUseViewActionInListings', ())
        browser_default = plone_utils.browserDefault(context)

        contentsMethod = context.contentValues

        show_all = self.request.get('show_all', '').lower() == 'true'
        pagesize = 20
        pagenumber = int(self.request.get('pagenumber', 1))
        start = (pagenumber - 1) * pagesize
        end = start + pagesize

        results = []
        for i, obj in enumerate(contentsMethod(self.contentFilter)):
            path = (
                getattr(obj, 'getPath', False)
                or "/".join(obj.getPhysicalPath()))

            # avoid creating unnecessary info for items outside the current
            # batch;  only the path is needed for the "select all" case...
            if not show_all and not start <= i < end:
                results.append(dict(path=path))
                continue

            if (i + 1) % 2 == 0:
                table_row_class = "draggable even"
            else:
                table_row_class = "draggable odd"

            url = obj.absolute_url()
            icon = plone_layout.getIcon(obj)
            type_class = 'contenttype-' + plone_utils.normalizeString(
                obj.portal_type)

            review_state = portal_workflow.getInfoFor(obj, 'review_state')
            state_class = 'state-' + plone_utils.normalizeString(review_state)
            relative_url = obj.absolute_url(relative=True)

            fti = portal_types.get(obj.portal_type)
            if fti is not None:
                type_title_msgid = fti.Title()
            else:
                type_title_msgid = obj.portal_type
            url_href_title = u'%s: %s' % (translate(type_title_msgid,
                                                    context=self.request),
                                          safe_unicode(obj.Description()))

            modified = plone_view.toLocalizedTime(
                obj.ModificationDate(), long_format=1)

            obj_type = obj.Type()
            is_folderish = getattr(
                aq_base(obj), 'isPrincipiaFolderish', False)
            if obj_type in use_view_action:
                view_url = url + '/view'
            elif is_folderish:
                view_url = url + "/folder_contents"
            else:
                view_url = url

            is_browser_default = len(browser_default[1]) == 1 and (
                obj.id == browser_default[1][0])

            results.append(dict(
                url=url,
                url_href_title=url_href_title,
                id=obj.getId(),
                quoted_id=urllib.quote_plus(obj.getId()),
                path=path,
                title_or_id=safe_unicode(pretty_title_or_id(plone_utils, obj)),
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
                folderish=is_folderish,
                relative_url=relative_url,
                view_url=view_url,
                table_row_class=table_row_class,
                is_expired=isExpired(obj),
            ))
        return results

    # BBB Plone 3 compat
    if hasattr(foldercontents.FolderContentsTable, 'items'):
        @property
        @instance.memoize
        def items(self):
            """BBB alias"""
            return self.folderitems()


class FolderContentsView(foldercontents.FolderContentsView):

    def contents_table(self):
        table = FolderContentsTable(aq_inner(self.context), self.request)
        return table.render()


if hasattr(foldercontents, 'FolderContentsKSSView'):
    # BBB Plone 4.2
    FolderContentsBrowserView = foldercontents.FolderContentsKSSView
else:
    FolderContentsBrowserView = foldercontents.FolderContentsBrowserView


class FolderContentsKSSView(FolderContentsBrowserView):
    table = FolderContentsTable
