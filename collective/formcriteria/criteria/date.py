from Products.ATContentTypes.criteria import date

from collective.formcriteria.criteria import common

class DateFormCriterion(
    common.FormCriterion, date.ATDateCriteria):
    __doc__ = date.ATDateCriteria.__doc__

    schema = date.ATDateCriteria.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['dateRange'], schema['operation'])
    schema['formFields'].widget.format = 'checkbox'

common.replaceCriterionRegistration(
    date.ATDateCriteria, DateFormCriterion)
