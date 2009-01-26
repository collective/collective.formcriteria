from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import list as list_

from collective.formcriteria.criteria import common

class ListFormCriterion(
    common.FormCriterion, list_.ATListCriterion):
    """A list form criterion"""

    meta_type = 'ListFormCriterion'
    archetype_name = 'List Form Criterion'
    shortDesc = 'Form: ' + list_.ATListCriterion.shortDesc

    schema = list_.ATListCriterion.schema.copy()
    schema['value'].widget.hide_form_label = True

criteria.registerCriterion(
    ListFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        list_.ATListCriterion.meta_type))
