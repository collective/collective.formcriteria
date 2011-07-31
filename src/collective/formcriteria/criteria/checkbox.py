from Products.ATContentTypes.criteria import selection
from Products.ATContentTypes.criteria import portaltype
from Products.ATContentTypes.criteria import reference

from collective.formcriteria.criteria import common
from collective.formcriteria.criteria import (
    selection as form_selection)


class FormCheckboxCriterion(
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

common.registerCriterion(FormCheckboxCriterion,
                         orig=form_selection.FormSelectionCriterion)


class FormPortalTypeCheckboxCriterion(
    common.FormCriterion, portaltype.ATPortalTypeCriterion):
    """A portal_types checkbox criterion"""

    archetype_name = 'Portal Types Checkbox Criterion'
    shortDesc = 'Check content types'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

common.registerCriterion(FormPortalTypeCheckboxCriterion,
                         orig=form_selection.FormPortalTypeCriterion)


class FormReferenceCheckboxCriterion(
    common.FormCriterion, reference.ATReferenceCriterion):
    """A reference checkbox criterion"""

    archetype_name = 'Portal Types Checkbox Criterion'
    shortDesc = 'Check referenced content'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'
    schema['value'].widget.hide_form_label = True
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

common.registerCriterion(FormReferenceCheckboxCriterion,
                         orig=form_selection.FormReferenceCriterion)
