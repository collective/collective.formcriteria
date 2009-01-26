from Products.ATContentTypes.criteria import simplestring

from collective.formcriteria.criteria import common

class SimpleStringFormCriterion(
    common.FormCriterion, simplestring.ATSimpleStringCriterion):
    __doc__ = simplestring.ATSimpleStringCriterion.__doc__

    schema = simplestring.ATSimpleStringCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])
    schema['formFields'].widget.format = 'checkbox'

common.replaceCriterionRegistration(
    simplestring.ATSimpleStringCriterion, SimpleStringFormCriterion)
