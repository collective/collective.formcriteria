from Products.ATContentTypes.criteria import date

from collective.formcriteria.criteria import common

class ATDateCriteria(
    common.FormCriterion, date.ATDateCriteria):
    __doc__ = date.ATDateCriteria.__doc__

    meta_type = 'ATFriendlyDateCriteria'

    schema = date.ATDateCriteria.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['dateRange'], schema['operation'])

common.replaceCriterionRegistration(
    date.ATDateCriteria, ATDateCriteria)
