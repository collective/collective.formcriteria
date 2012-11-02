import StringIO
import urlparse

import DateTime

from plone.testing import z2
from plone.app import testing

from Products.CMFCore.utils import getToolByName

from collective import formcriteria
from collective.formcriteria.portlet import portlet


def setATDateWidget(control, datetime, field, form='form'):
    name = form + '_' + field

    setATDateControl(control, datetime, name, 'year', zfill=4)
    setATDateControl(control, datetime, name, 'month')
    setATDateControl(control, datetime, name, 'day')
    setATDateControl(control, datetime, name, 'hour')
    setATDateControl(control, datetime, name, 'minute')

    ctl = control.getControl(name=name)
    ctl.value = str(datetime)
    return ctl


def setATDateControl(control, datetime, name, unit, zfill=2):
    value = getattr(datetime, unit)
    if callable(value):
        value = value()
    value = str(value)

    ctl = control.getControl(name=name + '_' + unit)

    if ctl.type == 'text':
        ctl = ctl
        ctl.value = value
    elif ctl.type == 'select':
        try:
            ctl = ctl.getControl(value=value.zfill(zfill))
        except LookupError:
            ctl = ctl.getControl(value=value)
        else:
            ctl.selected = True

    return ctl


def export(portal, context, request, url):
    environ_orig = request.environ
    form_orig = request.form.copy()
    other_orig = request.other.copy()
    stdout_orig = request.response.stdout
    stdout = StringIO.StringIO()
    getattr(request, '__annotations__', {}).clear()
    try:
        request.environ['QUERY_STRING'] = urlparse.urlsplit(
            url).query
        request.response.stdout = stdout
        request.processInputs()
        testing.login(portal, testing.TEST_USER_NAME)
        export_view = context.restrictedTraverse('export')
        export_view()
    finally:
        request.response.stdout = stdout_orig
        request.environ.clear()
        request.environ.update(environ_orig)
        request.form.clear()
        request.form.update(form_orig)
        request.other.clear()
        request.other.update(other_orig)
        testing.logout()
    return stdout.getvalue()


class FormcriteriaFixture(testing.PloneSandboxLayer):
    """Install collective.formcriteria"""

    defaultBases = (testing.PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        z2.installProduct(app, 'Products.PythonScripts')
        self.loadZCML('testing.zcml', package=formcriteria)
        z2.installProduct(app, 'collective.formcriteria')

    def setUpPloneSite(self, portal):
        from Products.CMFPlone import factory
        self.applyProfile(portal, factory._DEFAULT_PROFILE)
        self.applyProfile(portal, factory._CONTENT_PROFILE)
        getToolByName(portal, 'portal_css').setDebugMode(True)
        getToolByName(portal, 'portal_javascripts').setDebugMode(True)

        # Creates a user's home folder.
        membership = getToolByName(portal, 'portal_membership')
        if not membership.getMemberareaCreationFlag():
            membership.setMemberareaCreationFlag()
        membership.createMemberArea(testing.TEST_USER_ID)
        if membership.getMemberareaCreationFlag():
            membership.setMemberareaCreationFlag()
        folder = membership.getHomeFolder(testing.TEST_USER_ID)

        # Allow normal users to add collections.
        portal.manage_permission(
            'Add portal topics', roles=['Member', 'Manager'],
            acquire=0)

        self.applyProfile(portal, 'collective.formcriteria:default')
        self.applyProfile(portal, 'collective.formcriteria:testing')

        z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
        getToolByName(portal, 'portal_workflow').doActionFor(folder, 'publish')
        z2.logout()

FORMCRITERIA_FIXTURE = FormcriteriaFixture()

FORMCRITERIA_INTEGRATION_TESTING = testing.IntegrationTesting(
    bases=(FORMCRITERIA_FIXTURE,), name="FormcriteriaFixture:Integration")
FORMCRITERIA_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(FORMCRITERIA_FIXTURE,), name="FormcriteriaFixture:Functional")


class ContentFixture(testing.PloneSandboxLayer):
    """Add some content"""

    defaultBases = (FORMCRITERIA_FIXTURE, )

    def setUpPloneSite(self, portal):
        self.now = DateTime.DateTime(str(DateTime.DateTime())[:10])
        tomorrow = self.now + 1

        testing.login(portal, testing.TEST_USER_NAME)
        membership = getToolByName(portal, 'portal_membership')
        folder = membership.getHomeFolder(testing.TEST_USER_ID)
        foo_event = folder[folder.invokeFactory(
            type_name='Event', effectiveDate=self.now - 3,
            startDate=tomorrow, endDate=tomorrow,
            id='foo-event-title', title='Foo Event Title',
            creators='foo_creator_id', text='foo' * 2000)]
        bar_document = folder[folder.invokeFactory(
            type_name='Document', effectiveDate=self.now - 2,
            id='bar-document-title', title='Bar Document Title',
            description='blah', subject=['bah', 'qux'],
            creators='foo_creator_id', text='bar' * 1000)]
        bar_document.foo_int = 0
        baz_event = folder[folder.invokeFactory(
            type_name='Event', effectiveDate=self.now,
            id='baz-event-title', title='Baz Event Title',
            startDate=tomorrow, endDate=tomorrow,
            # More relevant for a "blah" search
            description='blah blah',
            subject=['qux', 'quux'],
            # BBB Plone 3, For Events eventType == subject
            eventType=['qux', 'quux'],
            creators='bar_creator_id')]
        baz_event.foo_int = 1

        z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
        portal.portal_workflow.doActionFor(foo_event, 'publish')
        portal.portal_workflow.doActionFor(
            bar_document, 'publish')
        portal.portal_workflow.doActionFor(baz_event, 'publish')
        bar_document.setModificationDate(self.now)
        bar_document.reindexObject(['modification_date'])
        z2.logout()

CONTENT_FIXTURE = ContentFixture()

CONTENT_INTEGRATION_TESTING = testing.IntegrationTesting(
    bases=(CONTENT_FIXTURE,), name="ContentFixture:Integration")
CONTENT_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(CONTENT_FIXTURE,), name="ContentFixture:Functional")


class TopicFixture(testing.PloneSandboxLayer):
    """Add a simple topic"""

    defaultBases = (CONTENT_FIXTURE, )

    def setUpPloneSite(self, portal):
        testing.login(portal, testing.TEST_USER_NAME)
        membership = getToolByName(portal, 'portal_membership')
        folder = membership.getHomeFolder(testing.TEST_USER_ID)
        foo_topic = folder[folder.invokeFactory(
            type_name='Topic', id='foo-topic-title',
            title='Foo Topic Title')]
        z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
        portal.portal_workflow.doActionFor(foo_topic, 'publish')
        z2.logout()

TOPIC_FIXTURE = TopicFixture()

TOPIC_INTEGRATION_TESTING = testing.IntegrationTesting(
    bases=(TOPIC_FIXTURE,), name="TopicFixture:Integration")
TOPIC_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(TOPIC_FIXTURE,), name="TopicFixture:Functional")


class CriteriaFixture(testing.PloneSandboxLayer):
    """Used for testing form criteria"""

    defaultBases = (TOPIC_FIXTURE, )

    def setUpPloneSite(self, portal):
        membership = getToolByName(portal, 'portal_membership')
        folder = membership.getHomeFolder(testing.TEST_USER_ID)
        topic = folder['foo-topic-title']
        site_path_len = len(portal.getPhysicalPath())
        manager = folder.restrictedTraverse(
            '++contextportlets++plone.rightcolumn')
        assignment = portlet.Assignment(
            target_collection='/'.join(
                topic.getPhysicalPath()[site_path_len:]))
        manager['foo-search-form-portlet'] = assignment

        testing.login(portal, testing.TEST_USER_NAME)
        folder[folder.invokeFactory(
            type_name='ATTopic', id='at-topic-title',
            title='AT Topic Title')]
        testing.logout()

CRITERIA_FIXTURE = CriteriaFixture()

CRITERIA_INTEGRATION_TESTING = testing.IntegrationTesting(
    bases=(CRITERIA_FIXTURE,), name="CriteriaFixture:Integration")
CRITERIA_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(CRITERIA_FIXTURE,), name="CriteriaFixture:Functional")


class ColumnsFixture(testing.PloneSandboxLayer):
    """Used for testing folder_contents columns"""

    defaultBases = (CONTENT_FIXTURE, )

    def setUpPloneSite(self, portal):
        self.applyProfile(
            portal, 'collective.formcriteria:formcriteria-columns')
        z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
        membership = getToolByName(portal, 'portal_membership')
        folder = membership.getHomeFolder(testing.TEST_USER_ID)
        folder.manage_pasteObjects(
            portal.templates.manage_copyObjects(['Topic']))
        folder.manage_renameObject('Topic', 'foo-topic-title')
        foo_topic = folder['foo-topic-title']
        foo_topic.update(title='Foo Topic Title')
        z2.logout()

COLUMNS_FIXTURE = ColumnsFixture()

COLUMNS_INTEGRATION_TESTING = testing.IntegrationTesting(
    bases=(COLUMNS_FIXTURE,), name="ColumnsFixture:Integration")
COLUMNS_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(COLUMNS_FIXTURE,), name="ColumnsFixture:Functional")


class ContentsFixture(testing.PloneSandboxLayer):
    """Used for testing folder contents"""

    defaultBases = (COLUMNS_FIXTURE, )

    def setUpPloneSite(self, portal):
        membership = getToolByName(portal, 'portal_membership')
        folder = membership.getHomeFolder(testing.TEST_USER_ID)
        foo_topic = folder['foo-topic-title']
        path_crit = foo_topic.addCriterion(
            'path', 'FormRelativePathCriterion')
        path_crit.setRecurse(True)
        sort_crit = foo_topic.addCriterion(
            'getPhysicalPath', 'FormSortCriterion')
        foo_topic.setLayout('folder_contents')

CONTENTS_FIXTURE = ContentsFixture()

CONTENTS_INTEGRATION_TESTING = testing.IntegrationTesting(
    bases=(CONTENTS_FIXTURE,), name="ContentsFixture:Integration")
CONTENTS_FUNCTIONAL_TESTING = testing.FunctionalTesting(
    bases=(CONTENTS_FIXTURE,), name="ContentsFixture:Functional")
