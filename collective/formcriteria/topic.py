from Products.Archetypes import atapi
from Products.ATContentTypes import interfaces as atct_ifaces
from Products.ATContentTypes import config 
from Products.ATContentTypes.content import topic
from Products.ATContentTypes import criteria
from Products.CMFPlone import CatalogTool

fake_sort_indices = {'unsorted': 'Relevance',
                     'sort_on': 'User Selected'}

class Topic(topic.ATTopic):
    """A collection supporting form criteria"""

    schema = topic.ATTopic.schema.copy() + atapi.Schema((
        atapi.StringField(
            'formLayout',
            default='atct_topic_view',
            vocabulary='getPossibleFormLayouts',
            widget=atapi.SelectionWidget(
                label=u'Form Results Layout',
                description=
                u'Select the display layout use for results.  '
                u'Used only with the "Search Form" layout')),
        ))

    def getPossibleFormLayouts(self):
        """Return all valid form results display laouts"""
        return atapi.DisplayList(
            layout for layout in self.getAvailableLayouts()
            if layout[0] != 'criteria_form')

    def criteriaByIndexId(self, indexId):
        catalog_tool = getattr(self, CatalogTool.CatalogTool.id)

        if indexId in fake_sort_indices:
            meta_type = indexId
        else:
            meta_type = catalog_tool.Indexes[indexId].meta_type

        results = criteria._criterionRegistry.criteriaByIndex(
            meta_type)
        return results

    def listSortCriteria(self):
        """Return a list of our sort criteria objects.
        """
        return [val for val in self.listCriteria() if
                atct_ifaces.IATTopicSortCriterion.isImplementedBy(val)]

    def getFriendlyName(self, index):
        """Get the friendly name for an index from the tool"""
        if index in fake_sort_indices:
            return fake_sort_indices[index]
        return getattr(self, config.TOOLNAME).getFriendlyName(index)
    
atapi.registerType(Topic, 'collective.formcriteria')
