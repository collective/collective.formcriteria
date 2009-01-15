"""Form criteria search form"""

from plone.memoize import view

from collective.formcriteria import interfaces

class SearchFormView(object):

    @view.memoize
    def formCriteria(self):
        return [
            criterion for criterion in self.context.listCriteria()
            if interfaces.IFormCriterion.providedBy(criterion)]
