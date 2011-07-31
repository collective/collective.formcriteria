from Products.Archetypes import atapi

from Products.ATContentTypes import permission
from Products.ATContentTypes.criteria import selection
from Products.ATContentTypes.criteria import portaltype
from Products.ATContentTypes.criteria import reference

from collective.formcriteria.criteria import common
from collective.formcriteria.criteria import (
    selection as form_selection)

field = atapi.StringField(
    'value',
    required=1,
    write_permission=permission.ChangeTopics,
    accessor="Value",
    vocabulary="getCurrentValues",
    widget=atapi.SelectionWidget(
        label=u'Value',
        description=u'Existing value.',
        format='select',
        hide_form_label=True))


class PulldownMixin(object):

    def getCriteriaItems(self):
        result = []

        if self.Value() is not '':
            result.append((self.Field(), self.Value()))

        return tuple(result)

    def getCurrentValues(self):
        """Insert an empty entry at the beginning since this is a
        single select field"""
        result = super(PulldownMixin, self).getCurrentValues()
        if isinstance(result, atapi.DisplayList):
            return atapi.DisplayList([('', '')]) + result
        else:
            return [''] + result


class FormPulldownCriterion(
    PulldownMixin, common.FormCriterion,
    selection.ATSelectionCriterion):
    """A pulldown criterion"""

    archetype_name = 'Pulldown Criterion'
    shortDesc = 'Select one value'

    schema = selection.ATSelectionCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema.addField(field)
    del schema['operator']
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])


common.registerCriterion(FormPulldownCriterion,
                         orig=form_selection.FormSelectionCriterion)


class FormPortalTypePulldownCriterion(
    PulldownMixin, common.FormCriterion,
    portaltype.ATPortalTypeCriterion):
    """A portal_types pulldown criterion"""

    archetype_name = 'Portal Types Pulldown Criterion'
    shortDesc = 'Select one content type'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema.addField(field)
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

common.registerCriterion(FormPortalTypePulldownCriterion,
                         orig=form_selection.FormPortalTypeCriterion)


class FormReferencePulldownCriterion(
    PulldownMixin, common.FormCriterion,
    reference.ATReferenceCriterion):
    """A reference pulldown criterion"""

    archetype_name = 'Portal Types Pulldown Criterion'
    shortDesc = 'Select one referenced content item'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema.addField(field)
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

common.registerCriterion(FormReferencePulldownCriterion,
                         orig=form_selection.FormReferenceCriterion)
