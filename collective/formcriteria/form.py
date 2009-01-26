"""Form criteria search form"""

from plone.memoize import view

def makeFormKey(self, crit_id, field_name):
    return 'form_%s_%s' % (crit_id, field_name)

class SearchFormView(object):

    def render(self, *args, **kw):
        if self.formCriteria():
            return super(SearchFormView, self).render(*args, **kw)
        return ''

    @view.memoize
    def formCriteria(self):
        return [
            criterion for criterion in self.context.listCriteria()
            if getattr(criterion, 'getFormFields', lambda : False)()]

    @view.memoize
    def criteriaFields(self):
        results = []
        for criterion in self.formCriteria():
            crit_id = criterion.getId()
            field = criterion.Field()
            index = self.context.portal_atct.getIndex(field)

            fields = []
            for field_name in criterion.getFormFields():
                field = criterion.getField(field_name)
                new_field = field.copy()
                new_field.write_permission = field.read_permission
                fields.append(new_field)

            result = {
                'id': crit_id,
                'field': field,
                'friendlyName': index.friendlyName or index.index,
                'description': index.description,
                'fields': fields,
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

    makeFormKey = makeFormKey
