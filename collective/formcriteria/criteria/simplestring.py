from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import simplestring

from collective.formcriteria.criteria import common

class SimpleStringFormCriterion(
    common.FormCriterion, simplestring.ATSimpleStringCriterion):
    """A simple string form criterion"""

    meta_type      = 'SimpleStringFormCriterion'
    archetype_name = 'Simple String Form Criterion'
    shortDesc = (
        'Form: ' + simplestring.ATSimpleStringCriterion.shortDesc)

    schema = simplestring.ATSimpleStringCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True

criteria.registerCriterion(
    SimpleStringFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        simplestring.ATSimpleStringCriterion.meta_type))
