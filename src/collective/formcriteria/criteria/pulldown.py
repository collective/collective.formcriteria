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

class FormPulldownCriterion(
    common.FormCriterion, selection.ATSelectionCriterion):
    """A pulldown criterion"""

    archetype_name = 'Pulldown Criterion'
    shortDesc = 'Select one value'

    schema = selection.ATSelectionCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema.addField(field)
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])

common.registerCriterion(FormPulldownCriterion,
                         orig=form_selection.FormSelectionCriterion)

class FormPortalTypePulldownCriterion(
    common.FormCriterion, portaltype.ATPortalTypeCriterion):
    """A portal_types pulldown criterion"""

    archetype_name = 'Portal Types Pulldown Criterion'
    shortDesc = 'Select one content type'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema.addField(field)
    schema['operator'].mode = 'r'
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'])

common.registerCriterion(FormPortalTypePulldownCriterion,
                         orig=form_selection.FormPortalTypeCriterion)

class FormReferencePulldownCriterion(
    common.FormCriterion, reference.ATReferenceCriterion):
    """A reference pulldown criterion"""

    archetype_name = 'Portal Types Pulldown Criterion'
    shortDesc = 'Select one referenced content item'

    schema = portaltype.ATPortalTypeCriterion.schema.copy(
        ) + common.FormCriterion.schema.copy()
    schema.addField(field)
    schema['formFields'].vocabulary = common.makeVocabularyForFields(
        schema['value'], schema['operator'])

common.registerCriterion(FormReferencePulldownCriterion,
                         orig=form_selection.FormReferenceCriterion)
