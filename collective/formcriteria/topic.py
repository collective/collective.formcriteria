from zope import interface

import AccessControl

from Products.Archetypes import atapi
from Products.ATContentTypes import interfaces as atct_ifaces
from Products.ATContentTypes import permission
from Products.ATContentTypes import config 
from Products.ATContentTypes.content import topic
from Products.ATContentTypes.tool import topic as topic_tool
from Products.ATContentTypes import criteria
from Products.CMFPlone import CatalogTool

from collective.formcriteria import interfaces
from collective.formcriteria.criteria import sort

class Topic(topic.ATTopic):
    """A collection supporting form criteria"""
    interface.implements(interfaces.IFormTopic)

    security = AccessControl.ClassSecurityInfo()

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

    sort_indices = {
        'unsorted': topic_tool.TopicIndex(
            index='unsorted',
            friendlyName='Relevance',
            description="Sorted by result weight",
            enabled=True,
            criteria=('FormSortCriterion',)),
        'sort_on': topic_tool.TopicIndex(
            index='sort_on',
            friendlyName='User Selected',
            description="The results sort order",
            enabled=True,
            criteria=('FormSortCriterion',))}

    sort_vocab = atapi.DisplayList([(sort.FormSortCriterion.meta_type,
                                     sort.FormSortCriterion.shortDesc)])
    
    def getPossibleFormLayouts(self):
        """Return all valid form results display laouts"""
        return atapi.DisplayList(
            layout for layout in self.getAvailableLayouts()
            if layout[0] != 'criteria_form')

    def criteriaByIndexId(self, indexId):
        catalog_tool = getattr(self, CatalogTool.CatalogTool.id)

        try:
            meta_type = catalog_tool.Indexes[indexId].meta_type
        except KeyError:
            if indexId in self.sort_indices:
                return self.sort_indices[indexId].criteria
            raise
        else:
            return criteria._criterionRegistry.criteriaByIndex(
                meta_type)

    def allowedCriteriaForField(self, field, display_list=False):
        """Add sort fields"""
        try:
            return super(Topic, self).allowedCriteriaForField(
                field, display_list=display_list)
        except AttributeError:
            if (field in self.sort_indices
                and self.validateAddCriterion(
                    field, sort.FormSortCriterion.meta_type)):
                if display_list:
                    return self.sort_vocab
                return [sort.FormSortCriterion.meta_type]

    security.declareProtected(permission.ChangeTopics, 'getIndex')
    def getIndex(self, name):
        """Get index data including sort indices"""
        tool = self.portal_atct
        try:
            return tool.getIndex(name)
        except AttributeError:
            if name in self.sort_indices:
                return self.sort_indices[name]
            raise

    def listFields(self):
        """Add sort fields"""
        return super(Topic, self
                     ).listFields() + [
            (key, value.friendlyName, value.description)
            for key, value in self.sort_indices.items()]

    def listSortCriteria(self):
        """Return a list of our sort criteria objects.
        """
        return [val for val in self.listCriteria() if
                atct_ifaces.IATTopicSortCriterion.isImplementedBy(val)]

    def getFriendlyName(self, index):
        """Get the friendly name for an index from the tool"""
        tool = getattr(self, config.TOOLNAME)
        try:
            tool.getIndex(index)
        except AttributeError:
            if index in self.sort_indices:
                return self.sort_indices[index].friendlyName
        return tool.getFriendlyName(index)        

    def addCriterion(self, field, criterion_type):
        """Make sure that criteria are properly initialized."""
        crit = super(Topic, self).addCriterion(field, criterion_type)
        crit.initializeArchetype()
        return crit
    
atapi.registerType(Topic, 'collective.formcriteria')
