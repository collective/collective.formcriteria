from DateTime import DateTime

from Products.ATContentTypes.criteria import daterange

from collective.formcriteria.criteria import common


class FormDateRangeCriterion(
    common.FormCriterion, daterange.ATDateRangeCriterion):
    __doc__ = daterange.ATDateRangeCriterion.__doc__

    schema = daterange.ATDateRangeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['start'].widget.show_hm = False
    schema['end'].widget.show_hm = False
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['start'], schema['end'])

    Value = daterange.ATDateRangeCriterion.Value

    def getDateTimeFormFieldValue(self, field_name, **kw):
        """
        Do DateTime Processing of form field values.
        """
        value = self.getFormFieldValue(field_name, **kw)

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

    def getStart(self, **kw):
        return self.getDateTimeFormFieldValue('start', **kw)

    def getRawStart(self, **kw):
        return self.getDateTimeFormFieldValue('start', raw=True, **kw)

    def getEnd(self, **kw):
        return self.getDateTimeFormFieldValue('end', **kw)

    def getRawEnd(self, **kw):
        return self.getDateTimeFormFieldValue('end', raw=True, **kw)

common.registerCriterion(
    FormDateRangeCriterion, orig=daterange.ATDateRangeCriterion)
