import Acquisition

from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import sort

from collective.formcriteria import topic
from collective.formcriteria.criteria import common

class ATSortCriterion(
    common.FormCriterion, sort.ATSortCriterion):
    __doc__ = sort.ATSortCriterion.__doc__

    schema = sort.ATSortCriterion.schema.copy()
    shortDesc      = 'Sort results'

    def getCriteriaItems(self):
        """Only use this sort if it is the default or is specified"""
        if self.Field() != 'unsorted' and (
            self.getId() in self.REQUEST or Acquisition.aq_base(self)
            is Acquisition.aq_base(self.listSortCriteria()[0])):
            return super(ATSortCriterion, self).getCriteriaItems()
        return ()
    
indices = criteria._criterionRegistry.indicesByCriterion(
    sort.ATSortCriterion.meta_type)
criteria.unregisterCriterion(sort.ATSortCriterion)
criteria.registerCriterion(
    ATSortCriterion,
    indices + tuple(topic.fake_sort_indices.keys()))
