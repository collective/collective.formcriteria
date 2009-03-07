from Products.ATContentTypes.criteria import relativepath

from collective.formcriteria.criteria import common

class FormRelativePathCriterion(
    common.FormCriterion, relativepath.ATRelativePathCriterion):
    __doc__ = relativepath.ATRelativePathCriterion.__doc__

    schema = relativepath.ATRelativePathCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['relativePath'], schema['recurse'])

common.registerCriterion(FormRelativePathCriterion,
                         orig=relativepath.ATRelativePathCriterion)
