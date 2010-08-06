import Acquisition

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.criteria import sort

from collective.formcriteria import interfaces
from collective.formcriteria.criteria import common


class FormSortCriterion(
    common.FormCriterion, sort.ATSortCriterion):
    __doc__ = sort.ATSortCriterion.__doc__

    schema = atapi.Schema((
        schemata.ATContentTypeSchema['title'],
        schemata.ATContentTypeSchema['description'],
        )) + sort.ATSortCriterion.schema.copy()
    shortDesc      = 'Sort results'

    def getCriteriaItems(self):
        """Only use this sort if it is the default or is specified"""
        topic = Acquisition.aq_parent(Acquisition.aq_inner(self))
        if not interfaces.IFormTopic.providedBy(topic) or (
            self.Field() != 'unsorted' and (
                self.getId() in self.REQUEST or
                Acquisition.aq_base(self) is Acquisition.aq_base(
                    topic.listSortCriteria()[0]))):
            return super(FormSortCriterion, self).getCriteriaItems()
        return ()

common.registerCriterion(FormSortCriterion, orig=sort.ATSortCriterion)
