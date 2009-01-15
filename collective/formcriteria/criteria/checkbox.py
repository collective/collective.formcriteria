from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import selection
from Products.ATContentTypes.criteria import portaltype
from Products.ATContentTypes.criteria import reference

from collective.formcriteria.criteria import common

class CheckboxFormCriterion(
    common.FormCriterion, selection.ATSelectionCriterion):
    """A checkbox form criterion"""

    meta_type = 'CheckboxFormCriterion'
    archetype_name = 'Checkbox Form Criterion'
    shortDesc = 'Form: Check values'

    schema = selection.ATSelectionCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'

criteria.registerCriterion(
    CheckboxFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        selection.ATSelectionCriterion.meta_type))

class PortalTypeCheckboxFormCriterion(
    common.FormCriterion, portaltype.ATPortalTypeCriterion):
    """A checkbox form criterion"""

    meta_type = 'PortalTypeCheckboxFormCriterion'
    archetype_name = 'Portal Types Checkbox Form Criterion'
    shortDesc = 'Form: Check content types'

    schema = portaltype.ATPortalTypeCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'
    schema['operator'].mode = 'r'

criteria.registerCriterion(
    PortalTypeCheckboxFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        portaltype.ATPortalTypeCriterion.meta_type))

class ReferenceCheckboxFormCriterion(
    common.FormCriterion, reference.ATReferenceCriterion):
    """A checkbox form criterion"""

    meta_type = 'ReferenceCheckboxFormCriterion'
    archetype_name = 'Portal Types Checkbox Form Criterion'
    shortDesc = 'Form: Check referenced content'

    schema = portaltype.ATPortalTypeCriterion.schema.copy()
    schema['value'].widget.format = 'checkbox'

criteria.registerCriterion(
    ReferenceCheckboxFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        reference.ATReferenceCriterion.meta_type))
