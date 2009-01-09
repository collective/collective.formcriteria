from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import simplestring

from collective.formcriteria.criteria import common

class SimpleStringFormCriterion(
    common.FormCriterion, simplestring.ATSimpleStringCriterion):
    """A simple string form criterion"""

    shortDesc = 'Form Text'

criteria.registerCriterion(
    SimpleStringFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        simplestring.ATSimpleStringCriterion.meta_type))
