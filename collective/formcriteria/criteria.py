from zope import interface

from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import simplestring

from collective.formcriteria import interfaces

class FormCriterion(object):
    """A criterion that generates a search form field."""
    interface.implements(interfaces.IFormCriterion)

    def getCriteriaItems(self):
        """Only return criteria items if no criterion was submitted"""
        if self.Field() in getattr(self, 'REQUEST', {}):
            return ()
        return super(FormCriterion, self).getCriteriaItems()
        

class SimpleStringFormCriterion(
    FormCriterion, simplestring.ATSimpleStringCriterion):
    """A simple string form criterion"""

    shortDesc = 'Form Text'

criteria.registerCriterion(
    SimpleStringFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        simplestring.ATSimpleStringCriterion.meta_type))
