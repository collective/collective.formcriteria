from Products.ATContentTypes.criteria import selection
from Products.ATContentTypes.criteria import portaltype
from Products.ATContentTypes.criteria import reference

from collective.formcriteria.criteria import common

class SelectionFormCriterion(
    common.FormCriterion, selection.ATSelectionCriterion):
    __doc__ = selection.ATSelectionCriterion.__doc__

    schema = selection.ATSelectionCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])
    schema['formFields'].widget.format = 'checkbox'

common.replaceCriterionRegistration(
    selection.ATSelectionCriterion, SelectionFormCriterion)

class PortalTypeSelectionFormCriterion(
    common.FormCriterion, portaltype.ATPortalTypeCriterion):
    __doc__ = portaltype.ATPortalTypeCriterion.__doc__

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True
    schema['operator'].mode = 'r'
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])
    schema['formFields'].widget.format = 'checkbox'

common.replaceCriterionRegistration(
    portaltype.ATPortalTypeCriterion, PortalTypeSelectionFormCriterion)

class ReferenceSelectionFormCriterion(
    common.FormCriterion, reference.ATReferenceCriterion):
    __doc__ = reference.ATReferenceCriterion.__doc__

    schema = reference.ATReferenceCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].possible_form_field = True
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])
    schema['formFields'].widget.format = 'checkbox'

common.replaceCriterionRegistration(
    reference.ATReferenceCriterion, ReferenceSelectionFormCriterion)
