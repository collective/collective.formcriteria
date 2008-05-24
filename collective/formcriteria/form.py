"""Form criteria search form"""

from zope import interface
from zope.cachedescriptors import property

from collective.formcriteria import interfaces

class ISearchFormView(interface.Interface):

    hasFormCriteria = interface.Attribute(
        'Has Form Criteria')

class SearchFormView(object):

    @property.Lazy
    def formCriteria(self):
        return [
            criterion for criterion in self.context.listCriteria()
            if interfaces.IFormCriterion.providedBy(criterion)]
