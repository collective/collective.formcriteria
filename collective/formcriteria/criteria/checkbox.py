from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import selection
from Products.ATContentTypes.criteria import portaltype
from Products.ATContentTypes.criteria import reference

from collective.formcriteria.criteria import common
from collective.formcriteria.criteria import (
    selection as form_selection)

class CheckboxFormCriterion(
    common.FormCriterion, selection.ATSelectionCriterion):
    """A checkbox criterion"""

    archetype_name = 'Checkbox Criterion'
    shortDesc = 'Check values'

    schema = selection.ATSelectionCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])

criteria.registerCriterion(
    CheckboxFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        form_selection.SelectionFormCriterion.meta_type))

class PortalTypeCheckboxFormCriterion(
    common.FormCriterion, portaltype.ATPortalTypeCriterion):
    """A portal_types checkbox criterion"""

    archetype_name = 'Portal Types Checkbox Criterion'
    shortDesc = 'Check content types'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'
    schema['value'].widget.hide_form_label = True
    schema['operator'].mode = 'r'
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

criteria.registerCriterion(
    PortalTypeCheckboxFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        form_selection.PortalTypeSelectionFormCriterion.meta_type))

class ReferenceCheckboxFormCriterion(
    common.FormCriterion, reference.ATReferenceCriterion):
    """A reference checkbox criterion"""

    archetype_name = 'Portal Types Checkbox Criterion'
    shortDesc = 'Check referenced content'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])

criteria.registerCriterion(
    ReferenceCheckboxFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        form_selection.ReferenceSelectionFormCriterion.meta_type))
