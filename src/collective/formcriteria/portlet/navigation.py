from plone.memoize import view

from Acquisition import aq_inner

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

from plone.app.portlets.portlets import navigation


class Renderer(navigation.Renderer):
    """Use Link remoteUrl if configured"""

    recurse = ViewPageTemplateFile('navigation_recurse.pt')

    @view.memoize
    def typesUseRemoteUrlInListings(self):
        context = aq_inner(self.context)
        properties = getToolByName(
            self.context, 'portal_properties').site_properties
        return getattr(properties, 'typesUseRemoteUrlInListings', ())
