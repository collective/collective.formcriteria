"""Form criteria search form"""

from plone.memoize import view

from collective.formcriteria import interfaces

class SearchFormView(object):

    @view.memoize
    def formCriteria(self):
        return [
            criterion for criterion in self.context.listCriteria()
            if interfaces.IFormCriterion.providedBy(criterion)]

    @view.memoize
    def criteriaFields(self):
        results = []
        for criterion in self.formCriteria():
            crit_id = criterion.getId()
            field = criterion.Field()
            index = self.context.portal_atct.getIndex(field)

            schematas = criterion.Schemata()
            fieldsets = [key for key in schematas.keys() if key != 'metadata']
            default_fieldset = (
                (not schematas or schematas.has_key('default'))
                and 'default' or fieldsets[0])
            fieldset = self.request.get('fieldset', default_fieldset)

            result = {
                'id': crit_id,
                'field': field,
                'friendlyName': index.friendlyName or index.index,
                'description': index.description,
                'fields': schematas[fieldset].fields(),
                'widget': criterion.widget,
                }

            results.append(result)
        return results

    def fields(self):
        results = []
        for criterion in self.criteriaFields():
            results.extend(criterion['fields'])
        return results

    def ifHead(self):
        return (
            getattr(self._parent, '_data', {}).get(
                'template_id') != 'criterion_edit_form'
            and self.formCriteria())
