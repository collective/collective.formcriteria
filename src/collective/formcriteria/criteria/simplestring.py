from Products.ATContentTypes.criteria import simplestring

from collective.formcriteria.criteria import common


class FormSimpleStringCriterion(
    common.FormCriterion, simplestring.ATSimpleStringCriterion):
    __doc__ = simplestring.ATSimpleStringCriterion.__doc__

    schema = simplestring.ATSimpleStringCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

common.registerCriterion(FormSimpleStringCriterion,
                         orig=simplestring.ATSimpleStringCriterion)
