from Products.Archetypes import atapi
from Products.ATContentTypes.content import topic

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
    
atapi.registerType(Topic, 'collective.formcriteria')
