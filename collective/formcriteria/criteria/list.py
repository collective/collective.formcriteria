from Products.ATContentTypes.criteria import list as list_

from collective.formcriteria.criteria import common

class ListFormCriterion(
    common.FormCriterion, list_.ATListCriterion):
    __doc__ = list_.ATListCriterion.__doc__
    """A list form criterion"""

    schema = list_.ATListCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])
    schema['formFields'].widget.format = 'checkbox'

common.replaceCriterionRegistration(
    list_.ATListCriterion, ListFormCriterion)
