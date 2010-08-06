from Products.ATContentTypes.criteria import simpleint

from collective.formcriteria.criteria import common


class FormSimpleIntCriterion(
    common.FormCriterion, simpleint.ATSimpleIntCriterion):
    __doc__ = simpleint.ATSimpleIntCriterion.__doc__

    schema = simpleint.ATSimpleIntCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['value2'], schema['direction'])

    def Value2(self, **kw):
        return self.getFormFieldValue('value2', **kw)

    def getRawValue2(self, **kw):
        return self.getFormFieldValue('value2', raw=True, **kw)

    def getDirection(self, **kw):
        return self.getFormFieldValue('direction', **kw)

common.registerCriterion(
    FormSimpleIntCriterion, orig=simpleint.ATSimpleIntCriterion)
