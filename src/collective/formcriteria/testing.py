import DateTime

from Testing import ZopeTestCase

from Products.Five import zcml, fiveconfigure

from collective.testcaselayer import ptc as tcl_ptc

from collective import formcriteria
from collective.formcriteria.portlet import portlet

class Layer(tcl_ptc.BasePTCLayer):
    """Install collective.formcriteria"""

    def afterSetUp(self):
        fiveconfigure.debug_mode = True
        zcml.load_config('testing.zcml', package=formcriteria)
        fiveconfigure.debug_mode = False

        ZopeTestCase.installPackage('collective.formcriteria')

        self.addProfile('collective.formcriteria:default')
        self.addProfile('collective.formcriteria:testing')

        self.loginAsPortalOwner()
        self.portal.portal_workflow.doActionFor(
            self.folder, 'publish')
        self.login()

layer = Layer([tcl_ptc.ptc_layer])

class ContentLayer(tcl_ptc.BasePTCLayer):
    """Add some content"""
    def afterSetUp(self):
        self.now = DateTime.DateTime('Jan 15, 2009')
        tomorrow = DateTime.DateTime()+1

        self.login()
        self.folder.invokeFactory(
            type_name='Event', effectiveDate=self.now-3,
            startDate=tomorrow, endDate=tomorrow,
            id='foo-event-title', title='Foo Event Title',
            creators='foo_creator_id', text='foo'*2000)
        self.folder.invokeFactory(
            type_name='Document', effectiveDate=self.now-2,
            id='bar-document-title', title='Bar Document Title',
            description='blah', subject=['bah', 'qux'],
            creators='foo_creator_id', text='bar'*1000)
        self.folder.invokeFactory(
            type_name='Event', effectiveDate=self.now,
            id='baz-event-title', title='Baz Event Title',
            startDate=tomorrow, endDate=tomorrow,
            # More relevant for a "blah" search
            description='blah blah',
            # For Events eventType == subject
            eventType=['qux', 'quux'],
            creators='bar_creator_id')

        self.loginAsPortalOwner()
        self.portal.portal_workflow.doActionFor(
            self.folder['bar-document-title'], 'publish')
        self.portal.portal_workflow.doActionFor(
            self.folder['baz-event-title'], 'publish')
        self.folder['bar-document-title'].setModificationDate(
            self.now)
        self.folder['bar-document-title'].reindexObject(
            ['modification_date'])
        self.login()

content_layer = ContentLayer([layer])

class TopicLayer(tcl_ptc.BasePTCLayer):
    """Add a simple topic"""

    def afterSetUp(self):
        self.loginAsPortalOwner()
        foo_topic = self.folder[self.folder.invokeFactory(
            type_name='Topic', id='foo-topic-title',
            title='Foo Topic Title')]
        self.portal.portal_workflow.doActionFor(foo_topic, 'publish')
        self.login()

topic_layer = TopicLayer([content_layer])

class CriteriaLayer(tcl_ptc.BasePTCLayer):
    """Used for testing form criteria"""

    def afterSetUp(self):
        topic = self.folder['foo-topic-title']
        site_path_len = len(self.portal.getPhysicalPath())
        manager = self.folder.restrictedTraverse(
            '++contextportlets++plone.rightcolumn')
        assignment = portlet.Assignment(
            target_collection='/'.join(
                topic.getPhysicalPath()[site_path_len:]))
        manager['foo-search-form-portlet'] = assignment

criteria_layer = CriteriaLayer([topic_layer])

class ColumnsLayer(tcl_ptc.BasePTCLayer):
    """Used for testing folder_contents columns"""

    def afterSetUp(self):
        self.addProfile('collective.formcriteria:columns')
        self.loginAsPortalOwner()
        self.folder.manage_pasteObjects(
            self.portal.templates.manage_copyObjects(['Topic']))
        self.folder.manage_renameObject('Topic', 'foo-topic-title')
        foo_topic = self.folder['foo-topic-title']
        foo_topic.update(title='Foo Topic Title')
        self.logout()
        
columns_layer = ColumnsLayer([content_layer])

class ContentsLayer(tcl_ptc.BasePTCLayer):
    """Used for testing folder contents"""

    def afterSetUp(self):
        foo_topic = self.folder['foo-topic-title']
        path_crit = foo_topic.addCriterion(
            'path', 'FormRelativePathCriterion')
        path_crit.setRecurse(True)
        sort_crit = foo_topic.addCriterion(
            'getPhysicalPath', 'FormSortCriterion')
        foo_topic.setLayout('folder_contents')

contents_layer = ContentsLayer([columns_layer])
