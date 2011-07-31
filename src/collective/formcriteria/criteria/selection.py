from Products.ATContentTypes.criteria import selection
from Products.ATContentTypes.criteria import portaltype
from Products.ATContentTypes.criteria import reference

from collective.formcriteria.criteria import common


class FormSelectionCriterion(
    common.FormCriterion, selection.ATSelectionCriterion):
    __doc__ = selection.ATSelectionCriterion.__doc__

    schema = selection.ATSelectionCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])

common.registerCriterion(
    FormSelectionCriterion, orig=selection.ATSelectionCriterion)


class FormPortalTypeCriterion(
    common.FormCriterion, portaltype.ATPortalTypeCriterion):
    __doc__ = portaltype.ATPortalTypeCriterion.__doc__

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

common.registerCriterion(
    FormPortalTypeCriterion, orig=portaltype.ATPortalTypeCriterion)


class FormReferenceCriterion(
    common.FormCriterion, reference.ATReferenceCriterion):
    __doc__ = reference.ATReferenceCriterion.__doc__

    schema = reference.ATReferenceCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].possible_form_field = True
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])

common.registerCriterion(
    FormReferenceCriterion, orig=reference.ATReferenceCriterion)
