from zope import interface
from zope import component

from DocumentTemplate.cDocumentTemplate import safe_callable

from Products.CMFCore import interfaces as cmf_ifaces
from Products.CMFCore.utils import getToolByName

from Products.ATContentTypes import criteria

from plone.indexer.interfaces import IIndexableObject

from collective.formcriteria.criteria import common
from collective.formcriteria.criteria import selection


class IContextCriterion(interface.Interface):
    """A criterion which pulls query terms from the context."""


class ICriteriaContext(interface.Interface):
    """Provide the current query criteria context."""


@interface.implementer(ICriteriaContext)
@component.adapter(IContextCriterion)
def getPublishedContext(context):
    parents = getattr(context, 'REQUEST', {}).get('PARENTS', ())
    for parent in parents:
        if cmf_ifaces.IContentish.providedBy(parent):
            return parent


class FormContextCriterion(selection.FormSelectionCriterion):
    __doc__ = IContextCriterion.__doc__
    interface.implements(IContextCriterion)

    archetype_name = 'Context Criterion'
    shortDesc = 'Values will be taken from the context'

    schema = selection.FormSelectionCriterion.schema.copy()
    schema['value'].widget.__dict__.update(
        visible=dict(view='invisible', edit='invisible'))

    def Value(self, **kw):
        catalog = getToolByName(self, 'portal_catalog')
        context = ICriteriaContext(self)
        wrapper = component.queryMultiAdapter(
            (context, catalog), IIndexableObject)
        if wrapper is None:
            wrapper = context

        value = getattr(wrapper, self.Field())
        if safe_callable(value):
            value = value()
        return value

common.registerCriterion(
    FormContextCriterion, indices=criteria.ALL_INDICES)
