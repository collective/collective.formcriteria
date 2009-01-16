from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import list as list_

from collective.formcriteria.criteria import common

class ListFormCriterion(
    common.FormCriterion, list_.ATListCriterion):
    """A list form criterion"""

    meta_type = 'ListFormCriterion'
    archetype_name = 'List Form Criterion'
    shortDesc = 'Form: ' + list_.ATListCriterion.shortDesc

criteria.registerCriterion(
    ListFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        list_.ATListCriterion.meta_type))
