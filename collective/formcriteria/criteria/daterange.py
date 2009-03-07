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

    def getStart(self, **kw):
        return self.getFormFieldValue('start', **kw)

    def getRawStart(self, **kw):
        return self.getFormFieldValue('start', raw=True, **kw)

    def getEnd(self, **kw):
        return self.getFormFieldValue('end', **kw)

    def getRawEnd(self, **kw):
        return self.getFormFieldValue('end', raw=True, **kw)

common.registerCriterion(
    FormDateRangeCriterion, orig=daterange.ATDateRangeCriterion)
