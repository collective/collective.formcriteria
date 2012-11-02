.. -*-doctest-*-

Context Criteria
================

A criterion which pulls the values from the context.  This can be
used with collection portlets such that the criterion's query values
will be taken from the context in which the portlet is rendered.  When
used in combination with the Subject/Categories field, for example,
the criterion would match content which have at least one of the
categories/subjects of the current context.

    >>> from plone.testing import z2
    >>> from plone.app  import testing

We start with a topic and two contexts with different
subjects/keywords/categories.

    >>> from Products.CMFCore.utils import getToolByName
    >>> portal = layer['portal']
    >>> membership = getToolByName(portal, 'portal_membership')
    >>> folder = membership.getHomeFolder(testing.TEST_USER_ID)
    >>> foo_topic = folder['foo-topic-title']
    >>> foo_event = folder['foo-event-title']
    >>> bar_document = folder['bar-document-title']

    >>> portal = layer['portal']
    >>> z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
    >>> foo_event.update(
    ...     subject=['foo'],
    ...     # BBB Plone 3, For Events eventType == subject
    ...     eventType=['foo'])
    >>> z2.logout()

Add a context criterion for the subject/keywords.

    >>> foo_topic.addCriterion(
    ...     'Subject', 'FormContextCriterion')
    <FormContextCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__Subject_FormContextCriterion>

Add a collection portlet that uses the topic.

    >>> from zope import component
    >>> from plone.i18n.normalizer import (
    ...     interfaces as normalizer_ifaces)
    >>> from plone.portlet.collection import collection
    >>> testing.login(portal, testing.TEST_USER_NAME)
    >>> manager = folder.restrictedTraverse(
    ...     '++contextportlets++plone.rightcolumn')
    >>> site_path_len = len(portal.getPhysicalPath())
    >>> assignment = collection.Assignment(
    ...     header='Collection Portlet',
    ...     target_collection='/'.join(
    ...         foo_topic.getPhysicalPath()[site_path_len:]))
    >>> name = component.getUtility(
    ...     normalizer_ifaces.IIDNormalizer).normalize(
    ...         assignment.title)
    >>> manager[name] = assignment
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

Open a browser as an anonymous user.  

    >>> from plone.testing import z2
    >>> from plone.app import testing
    >>> browser = z2.Browser(layer['app'])
    >>> browser.handleErrors = False

View one of the contexts with subjects/keywords/categories.  Only
items matching the subjects/keywords/categories of the context are
listed.

    >>> browser.open(bar_document.absolute_url())
    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

View another context with different subjects/keywords/categories.  Now
the items matching the subjects/keywords/categories of this context
are listed.

    >>> browser.open(foo_event.absolute_url())
    >>> browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError
