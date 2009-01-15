from zope import interface

from collective.formcriteria import interfaces

missing = object()

class FormCriterion(object):
    """A criterion that generates a search form field."""
    interface.implements(interfaces.IFormCriterion)

    def getFormFieldValue(self, field_name, REQUEST=None, **kw):
        """
        Get the field value from the request.

        Fall back to the criterion value.
        """
        if REQUEST is None:
            REQUEST = self.REQUEST

        field = self.getField(field_name)
        full_name = self.getId() + '.' + field_name

        # Remove the criterion ids from and relevant request keys
        form = dict(
            (key.replace(full_name, field_name, 1), REQUEST[key])
            for key in REQUEST.keys() if field_name in key)

        if not form:
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
