"""Form criteria search form"""

from zope import component

from plone.memoize import view
from plone.portlets import interfaces as portelts_ifaces

from collective.formcriteria import interfaces


def makeFormKey(self, crit_id, field_name):
    return 'form_%s_%s' % (crit_id, field_name)


class SearchFormView(object):

    def formCriteria(self):
        return (
            crit for crit in self.context.listCriteria()
            if getattr(crit, 'getFormFields', lambda: False)())

    @view.memoize
    def criteriaFields(self):
        criteria = {}
        fields = set()

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
            fields.add(field)
            criteria[field] = {
                'id': crit_id,
                'field': field,
                'friendlyName': criterion.getField('title').get(criterion) or index.friendlyName or index.index,
                'description': criterion.getField('description').get(criterion) or index.description,
                'fields': crit_fields,
                'criterion': criterion,
                }

        return fields, criteria

    makeFormKey = makeFormKey

    def action(self):
        return '%s/%s' % (self.context.absolute_url(),
                          self.context.getFormLayout())


class SearchFormHeadView(object):

    portlet_managers = ('plone.leftcolumn', 'plone.rightcolumn')

    def render(self):
        if self.fields():
            return super(SearchFormHeadView, self).render()
        return u''

    def collections(self):
        results = {}
        for portlet in self.portlets():
            collection = portlet.collection()
            results[collection.getPhysicalPath()] = collection
        if interfaces.IFormTopic.providedBy(self.context):
            results[self.context.getPhysicalPath()] = self.context
        return results.values()

    def portlets(self):
        results = []
        for name in self.portlet_managers:
            manager = component.getUtility(
                portelts_ifaces.IPortletManager, name=name)
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
        for collection in self.collections():
            criteria_form = collection.restrictedTraverse('@@criteria_form')
            criteria = criteria_form.criteriaFields()[1]
            for criterion in criteria.values():
                results.extend(criterion['fields'])
        return results


class SearchFormDashboardHeadView(SearchFormHeadView):

    portlet_managers = SearchFormHeadView.portlet_managers + (
        'plone.dashboard1', 'plone.dashboard2',
        'plone.dashboard3', 'plone.dashboard4',) 
