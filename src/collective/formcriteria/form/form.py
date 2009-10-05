"""Form criteria search form"""

from zope import component

from plone.memoize import view
from plone.portlets import interfaces as portelts_ifaces

from collective.formcriteria import interfaces

def makeFormKey(self, crit_id, field_name):
    return 'form_%s_%s' % (crit_id, field_name)

class SearchFormView(object):

    def getFormCriteria(self, collection):
        return (
            criterion for criterion in collection.listCriteria()
            if getattr(criterion, 'getFormFields', lambda : False)())

    @view.memoize
    def formCriteria(self):
        return list(self.getFormCriteria(self.context))

    @view.memoize
    def criteriaFields(self):
        criteria = {}
        fields = []
        
        for criterion in self.formCriteria():
            field = criterion.Field()
            index = self.context.portal_atct.getIndex(field)

            crit_fields = []
            for field_name in criterion.getFormFields():
                crit_field = criterion.getField(field_name)
                new_field = crit_field.copy()
                new_field.write_permission = crit_field.read_permission
                crit_fields.append(new_field)

            crit_id = criterion.getId()
            fields.append(field)
            criteria[field] = {
                'id': crit_id,
                'field': field,
                'friendlyName': index.friendlyName or index.index,
                'description': index.description,
                'fields': crit_fields,
                'widget': criterion.widget,
                }

        return fields, criteria

    makeFormKey = makeFormKey

    def action(self):
        return '%s/%s' % (self.context.absolute_url(),
                          self.context.getFormLayout())

class SearchFormHeadView(SearchFormView):

    def render(self):
        if self.fields():
            return super(SearchFormHeadView, self).render()
        return u''

    @view.memoize
    def formCriteria(self):
        results = []
        if interfaces.IFormTopic.providedBy(self.context):
            results.extend(self.getFormCriteria(self.context))
        for portlet in self.portlets():
            results.extend(self.getFormCriteria(portlet.collection()))
        return results

    @view.memoize
    def portlets(self):
        results = []
        for _, manager in component.getUtilitiesFor(
            portelts_ifaces.IPortletManager):
            renderer = manager(
                self.context, self.request, self._parent)
            if hasattr(renderer, 'portletsToShow'):
                for portlet in renderer.portletsToShow():
                    if interfaces.IFormCriteriaPortlet.providedBy(
                        portlet['renderer']):
                        results.append(portlet['renderer'])
        return results

    @view.memoize
    def fields(self):
        results = []
        for criterion in self.criteriaFields()[1].values():
            results.extend(criterion['fields'])
        return results
