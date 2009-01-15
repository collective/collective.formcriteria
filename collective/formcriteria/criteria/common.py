from zope import interface

from collective.formcriteria import interfaces

missing = object()

class FormCriterion(object):
    """A criterion that generates a search form field."""
    interface.implements(interfaces.IFormCriterion)

    def getFormFieldValue(self, field_name, **kw):
        """
        Get the field value from the request.

        Fall back to the criterion value.
        """
        field = self.getField(field_name)
        record = self.REQUEST.get(self.getId(), missing)

        if record is missing:
            return field.get(self, **kw)

        result = field.widget.process_form(
            self, field, record,
            empty_marker=missing, emptyReturnsMarker=True)

        if result is missing:
            return field.get(self, **kw)

        value, mutator_kw = result
        return value

    def Value(self, **kw):
        return self.getFormFieldValue('value', **kw)
