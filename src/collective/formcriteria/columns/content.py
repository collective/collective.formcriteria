
from Acquisition import aq_parent
from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi
from Products.ATContentTypes import permission

from collective.formcriteria import contained


class TopicColumns(contained.NonRefCatalogMixin,
                  atapi.OrderedBaseFolder):
    """Contains folder_contents table columns"""

    security = ClassSecurityInfo()

    meta_type = portal_type = 'TopicColumns'
    archetype_name = 'Topic Columns'

atapi.registerType(TopicColumns, 'collective.formcriteria')

column_schema = atapi.Schema((
    atapi.StringField(
        'id',
        required=1,
        write_permission=permission.ChangeTopics,
        vocabulary='listMetaDataVocab',
        enforceVocabulary=True,
        widget=atapi.SelectionWidget(
            label=u'Field',
            description=u"Select the catalog/brains metadata for the column",
            visible={'view': 'invisible'})),
    atapi.BooleanField(
        'link',
        write_permission=permission.ChangeTopics,
        widget=atapi.BooleanWidget(
            label=u'Link to the Item?',
            description=u'Should the cells for this column '
            'render a content type icon and a link to the item?')),
    atapi.BooleanField(
        'sum',
        write_permission=permission.ChangeTopics,
        widget=atapi.BooleanWidget(
            label=u'Sum Total?',
            description=u'Should the cells for this column be added '
            'together to calculate a total for the column?')),
    atapi.StringField(
        'expression',
        write_permission=permission.ChangeTopics,
        widget=atapi.StringWidget(
            label=u'Cell Expression',
            description=u"""\
If the cell contents for this column should be something other than
the 'Field' value, enter a TAL expression here.""")),
    atapi.StringField(
        'sort',
        write_permission=permission.ChangeTopics,
        vocabulary='listSortCriteriaVocab',
        enforceVocabulary=True,
        widget=atapi.SelectionWidget(
            label=u'Sort Criterion',
            description=u"""\
Select a sort criterion on which to sort when the column header is
clicked.  If the required index is not in the list, add a sort
criterion for the index first.""")),
    atapi.StringField(
        'filter',
        write_permission=permission.ChangeTopics,
        vocabulary='listQueryCriteriaVocab',
        enforceVocabulary=True,
        widget=atapi.SelectionWidget(
            label=u'Filter Criterion',
            description=u"""\
Select a query criterion on which to filter for this column.  If the
required index is not in the list, add a query criterion for the index
first.""")),
    ))


class TopicColumn(contained.NonRefCatalogMixin,
                  atapi.BaseContentMixin):
    """A folder_contents table column"""

    security = ClassSecurityInfo()

    meta_type = portal_type = 'TopicColumn'
    archetype_name = 'Topic Column'

    schema = atapi.BaseContentMixin.schema.copy() + column_schema
    schema['title'].widget.visible = dict(
        view='invisible', edit='invisible')

    def Field(self):
        """Return the field name without the '-column' suffix"""
        return self.getId()[:-7]

    def Title(self, **kw):
        title = self.Schema()['title'].get(self, **kw)
        if title:
            return title
        return self.Vocabulary('id')[0].getValue(self.getId())

    def listMetaDataVocab(self):
        """Append '-column' suffix to avoid id clashes"""
        fields = aq_parent(aq_parent(self)).listMetaDataFields()
        fields.add('getPath', 'URL')
        return atapi.DisplayList(
            (key + '-column', fields.getValue(key)) for key in fields)

atapi.registerType(TopicColumn, 'collective.formcriteria')
