from Products.ATContentTypes.criteria import list as list_

from collective.formcriteria.criteria import common

class ListFormCriterion(
    common.FormCriterion, list_.ATListCriterion):
    __doc__ = list_.ATListCriterion.__doc__

    schema = list_.ATListCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])

common.replaceCriterionRegistration(
    list_.ATListCriterion, ListFormCriterion)
