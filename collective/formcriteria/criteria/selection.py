from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import selection
from Products.ATContentTypes.criteria import portaltype
from Products.ATContentTypes.criteria import reference

from collective.formcriteria.criteria import common

class SelectionFormCriterion(
    common.FormCriterion, selection.ATSelectionCriterion):
    """A selection form criterion"""

    meta_type = 'SelectionFormCriterion'
    archetype_name = 'Selection Form Criterion'
    shortDesc = 'Form: ' + selection.ATSelectionCriterion.shortDesc

criteria.registerCriterion(
    SelectionFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        selection.ATSelectionCriterion.meta_type))

class PortalTypeSelectionFormCriterion(
    common.FormCriterion, portaltype.ATPortalTypeCriterion):
    """A portal_types form criterion"""

    meta_type = 'PortalTypeSelectionFormCriterion'
    archetype_name = 'Portal Types Selection Form Criterion'
    shortDesc = 'Form: ' + portaltype.ATPortalTypeCriterion.shortDesc

    schema = portaltype.ATPortalTypeCriterion.schema.copy()
    schema['operator'].mode = 'r'

criteria.registerCriterion(
    PortalTypeSelectionFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        portaltype.ATPortalTypeCriterion.meta_type))

class ReferenceSelectionFormCriterion(
    common.FormCriterion, reference.ATReferenceCriterion):
    """A selection form criterion"""

    meta_type = 'ReferenceSelectionFormCriterion'
    archetype_name = 'Portal Types Selection Form Criterion'
    shortDesc = 'Form: ' + reference.ATReferenceCriterion.shortDesc

criteria.registerCriterion(
    ReferenceSelectionFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        reference.ATReferenceCriterion.meta_type))
