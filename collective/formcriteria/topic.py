from Products.Archetypes import atapi
from Products.ATContentTypes.content import topic
from Products.ATContentTypes import criteria
from Products.CMFPlone import CatalogTool

fake_sort_indices = ('unsorted', 'sort_on')

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
    
atapi.registerType(Topic, 'collective.formcriteria')
