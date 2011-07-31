from Products.ATContentTypes.criteria import path

from collective.formcriteria.criteria import common


class FormPathCriterion(
    common.FormCriterion, path.ATPathCriterion):
    __doc__ = path.ATPathCriterion.__doc__

    schema = path.ATPathCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['recurse'])

    def Recurse(self, **kw):
        return self.getFormFieldValue('recurse', **kw)

common.registerCriterion(
    FormPathCriterion, orig=path.ATPathCriterion)
