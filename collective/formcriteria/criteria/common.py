from zope import interface

from collective.formcriteria import interfaces

class FormCriterion(object):
    """A criterion that generates a search form field."""
    interface.implements(interfaces.IFormCriterion)

    def getCriteriaItems(self):
        """Only return criteria items if no criterion was submitted"""
        if self.Field() in getattr(self, 'REQUEST', {}):
            return ()
        return super(FormCriterion, self).getCriteriaItems()
