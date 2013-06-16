from zope import interface

from Products.CMFCore.utils import getToolByName
from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes import criteria
from Products.ATContentTypes import interfaces as atct_ifaces

from collective.formcriteria import interfaces
from collective.formcriteria.form import form

missing = object()


def makeVocabularyForFields(*fields):
    return atapi.DisplayList(
        (field.getName(), field.widget.label)
        for field in fields)


def registerCriterion(criterion, orig=None, indices=()):
    if orig is not None:
        indices = criteria._criterionRegistry.indicesByCriterion(
            orig.meta_type)

    if isinstance(indices, str):
        indices = (indices,)
    indices = tuple(indices)

    if indices == ():
        indices = criteria.ALL_INDICES

    implementedBy = getattr(
        atct_ifaces.IATTopicCriterion, 'implementedBy', None)
    if implementedBy is None:
        # BBB Plone 3
        implementedBy = (
            atct_ifaces.IATTopicCriterion.isImplementedByInstancesOf)
    assert implementedBy(criterion)
    atapi.registerType(criterion, 'collective.formcriteria')

    crit_id = criterion.meta_type
    criteria._criterionRegistry[crit_id] = criterion
    criteria._criterionRegistry.portaltypes[
        criterion.portal_type] = criterion

    criteria._criterionRegistry.criterion2index[crit_id] = indices
    for index in indices:
        value = criteria._criterionRegistry.index2criterion.get(
            index, ())
        criteria._criterionRegistry.index2criterion[
            index] = value + (crit_id,)


class FormCriterion(object):
    """A criterion that generates a search form field."""
    interface.implements(interfaces.IFormCriterion)

    schema = atapi.Schema((
        schemata.ATContentTypeSchema['title'],
        schemata.ATContentTypeSchema['description'],
        atapi.LinesField(
            'formFields',
            widget=atapi.MultiSelectionWidget(
                label=u'Form Fields',
                description=(
                    u'Select any fields for this criterion that should'
                    u'appear on a search form'),
                format='checkbox')),))

    makeFormKey = form.makeFormKey

    def Title(self):
        """Retrieve the title from the ATCT configuration"""
        return self.title or getToolByName(self, 'portal_atct').getFriendlyName(
            self.Field())

    def getFormFieldValue(self, field_name, raw=False, REQUEST=None,
                          **kw):
        """
        Get the field value from the request.

        Fall back to the criterion value.
        """
        field = self.getField(field_name)
        if field_name not in self.getFormFields():
            if raw:
                return field.getRaw(self, **kw)
            return field.get(self, **kw)

        if REQUEST is None:
            REQUEST = self.REQUEST

        full_name = self.makeFormKey(self.getId(), field_name)

        # Remove the criterion ids from and relevant request keys
        form = dict(
            (key.replace(full_name, field_name, 1), REQUEST[key])
            for key in REQUEST.keys() if key.startswith(full_name))

        if not form:
            if raw:
                return field.getRaw(self, **kw)
            return field.get(self, **kw)

        result = field.widget.process_form(
            self, field, form,
            empty_marker=missing, emptyReturnsMarker=True)

        if result is missing:
            if raw:
                return field.getRaw(self, **kw)
            return field.get(self, **kw)

        value, mutator_kw = result
        return value

    def Value(self, **kw):
        return self.getFormFieldValue('value', **kw)

    def getRawValue(self, **kw):
        return self.getFormFieldValue('value', raw=True, **kw)

    def getOperator(self, **kw):
        return self.getFormFieldValue('operator', **kw)
