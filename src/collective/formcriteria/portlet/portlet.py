from zope import interface
from zope import schema
from zope.formlib import form
from zope.cachedescriptors import property
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.vocabularies import catalog
from plone.app.form.widgets import uberselectionwidget
from plone.portlets import interfaces as portlets_ifaces
from plone.portlet.collection import collection
from plone.portlet.collection import PloneMessageFactory as _

from Products.ATContentTypes import interface as atct_ifaces

from collective.formcriteria import interfaces


class ICriteriaFormPortlet(portlets_ifaces.IPortletDataProvider):
    """A search form based on the criteria in a collection."""

    header = schema.TextLine(
        title=_(u"Portlet header"),
        description=_(u"Title of the rendered portlet"),
        required=True)

    target_collection = schema.Choice(
        title=_(u"Target collection"),
        description=_(
            u"Find the collection which provides the items to list"),
        required=True,
        source=catalog.SearchableTextSourceBinder(
            {'object_provides': atct_ifaces.IATTopic.__identifier__},
            default_query='path:'))


class Assignment(collection.Assignment):
    interface.implements(ICriteriaFormPortlet)


class Renderer(collection.Renderer):
    """Portlet renderer."""
    interface.implements(interfaces.IFormCriteriaPortlet)

    render = ViewPageTemplateFile('portlet.pt')

    @property.Lazy
    def available(self):
        return (self.__parent__.__name__ != 'criteria_form'
                and self.form.criteriaFields()[0])

    @property.Lazy
    def form(self):
        return self.collection().restrictedTraverse('criteria_form')


form_fields = form.Fields(ICriteriaFormPortlet)
form_fields[
    'target_collection'
    ].custom_widget = uberselectionwidget.UberSelectionWidget

description = (
    u'A search form based on the criteria in a collection')


class AddForm(collection.AddForm):
    form_fields = form_fields

    label = u'Add Search Form Portlet'
    description = description

    def create(self, data):
        return Assignment(**data)


class EditForm(collection.EditForm):
    form_fields = form_fields

    label = u'Edit Search Form Portlet'
    description = description
