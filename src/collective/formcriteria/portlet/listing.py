from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.portlet.collection import collection

class Renderer(collection.Renderer):
    """Use the richer template"""

    render = ViewPageTemplateFile('listing.pt')
