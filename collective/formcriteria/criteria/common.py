from zope import interface

from Products.Archetypes import atapi
from Products.ATContentTypes import criteria

from collective.formcriteria import interfaces
from collective.formcriteria import form

missing = object()

def makeVocabularyForFields(*fields):
    return atapi.DisplayList(
        (field.getName(), field.widget.label)
        for field in fields)

def registerCriterion(class_, orig):
    return criteria.registerCriterion(
        class_,
        criteria._criterionRegistry.indicesByCriterion(
            orig.meta_type))

class FormCriterion(object):
    """A criterion that generates a search form field."""
    interface.implements(interfaces.IFormCriterion)

    schema = atapi.Schema((
        atapi.LinesField(
            'formFields',
            widget=atapi.MultiSelectionWidget(
                label=u'Form Fields',
                description=
                u'Select any fields for this criterion that should'
                u'appear on a search form',
                format='checkbox')),))

    makeFormKey = form.makeFormKey

    def getFormFieldValue(self, field_name, raw=False, REQUEST=None,
                          **kw):
        """
        Get the field value from the request.

        Fall back to the criterion value.
        """
        if REQUEST is None:
            REQUEST = self.REQUEST

        field = self.getField(field_name)
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
            return field.get(self, **kw)

        value, mutator_kw = result
        return value

    def Value(self, **kw):
        return self.getFormFieldValue('value', **kw)

    def getRawValue(self, **kw):
        return self.getFormFieldValue('value', raw=True, **kw)
