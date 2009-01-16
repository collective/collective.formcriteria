from Products.ATContentTypes import criteria
from Products.ATContentTypes.criteria import daterange

from collective.formcriteria.criteria import common

class DateRangeFormCriterion(
    common.FormCriterion, daterange.ATDateRangeCriterion):
    """A date range form criterion"""

    meta_type      = 'DateRangeFormCriterion'
    archetype_name = 'Date Range Form Criterion'
    shortDesc = 'Form: ' + daterange.ATDateRangeCriterion.shortDesc

    Value = daterange.ATDateRangeCriterion.Value

    def getStart(self, **kw):
        return self.getFormFieldValue('start', **kw)

    def getEnd(self, **kw):
        return self.getFormFieldValue('end', **kw)

criteria.registerCriterion(
    DateRangeFormCriterion,
    criteria._criterionRegistry.indicesByCriterion(
        daterange.ATDateRangeCriterion.meta_type))
