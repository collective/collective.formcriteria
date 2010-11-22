from DateTime import DateTime

from Products.ATContentTypes.criteria import date

from collective.formcriteria.criteria import common


class DateCriterion(common.FormCriterion):
    """A criterion that generates a DateTime search form field."""

    def getFormFieldValue(self, field_name, **kw):
        """
        Do DateTime Processing of form field values.
        """
        value = super(DateCriterion, self).getFormFieldValue(
            field_name, **kw)

        # From Products.Archetypes.Field.DateTimeField.set()
        # Unfortunately, this is another instance of Archetypes
        # failure to practice proper separation between the field and
        # the widget.  In this case, the field mutator does the type
        # conversion for the value returned by the widget so we have
        # to reproduce it here.
        if not value:
            value = None
        elif not isinstance(value, DateTime):
            try:
                # Convert value to non-ISO8601 representation (YYYY/MM/DD).
                # DateTime uses local timezone for non-ISO8601 strings,
                # otherwise it uses timezone naive conversion.
                # see http://dev.plone.org/plone/ticket/10141
                value = DateTime(value.replace('-', '/', 2))
            except DateTime.DateTimeError:
                value = None

        return value


class FormDateCriterion(
    DateCriterion, date.ATDateCriteria):
    __doc__ = date.ATDateCriteria.__doc__

    schema = date.ATDateCriteria.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['dateRange'], schema['operation'])

common.registerCriterion(
    FormDateCriterion, orig=date.ATDateCriteria)
