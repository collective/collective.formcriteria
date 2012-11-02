.. -*-doctest-*-

==================
Collection Portlet
==================

The collection portlet included with collective.formcriteria uses
Plone's folder_listing template to render the contents.  This provides
a richer available data structure including descriptions, event
handling, author information, etc..

Add a criterion to the topic.

    >>> from Products.CMFCore.utils import getToolByName
    >>> portal = layer['portal']
    >>> membership = getToolByName(portal, 'portal_membership')

    >>> from plone.app import testing
    >>> folder = membership.getHomeFolder(testing.TEST_USER_ID)
    >>> foo_topic = folder['foo-topic-title']
    >>> path_crit = foo_topic.addCriterion(
    ...     'path', 'FormRelativePathCriterion')
    >>> path_crit.setRecurse(True)

Chang the folder layout to be something other than the folder_listing
template to differentiate output.

    >>> folder.setLayout('folder_summary_view')

    >>> import transaction
    >>> transaction.commit()

Login as a user that can manage portlets.

    >>> from plone.testing import z2
    >>> from plone.app import testing
    >>> owner_browser = z2.Browser(layer['app'])
    >>> owner_browser.handleErrors = False
    >>> owner_browser.open(portal.absolute_url())
    >>> owner_browser.getLink('Log in').click()
    >>> owner_browser.getControl(
    ...     'Login Name').value = testing.SITE_OWNER_NAME
    >>> owner_browser.getControl(
    ...     'Password').value = testing.TEST_USER_PASSWORD
    >>> owner_browser.getControl('Log in').click()

Add the collection listing portlet to the folder.

    >>> owner_browser.open(folder.absolute_url())
    >>> owner_browser.getLink('Manage portlets').click()
    >>> owner_browser.getControl(
    ...     'Collection portlet', index=1).selected = True
    >>> owner_browser.getForm(index=3).submit() # manually w/o JS
    >>> print owner_browser.contents
    <...
    ...Add Collection Portlet...

    >>> portal = layer['portal']
    >>> header = owner_browser.getControl('Portlet header')
    >>> header.value = 'Foo Collection Listing Portlet Title'
    >>> foo_topic_path = '/'.join(
    ...     ('',)+ foo_topic.getPhysicalPath()[
    ...         len(portal.getPhysicalPath()):])
    >>> header.mech_form.new_control(
    ...     type='checkbox', name="form.target_collection",
    ...     attrs=dict(checked='checked', value=foo_topic_path))
    >>> owner_browser.getControl('Save').click()
    >>> print owner_browser.contents
    <...
    ...Foo Collection Listing Portlet Title...

Add a link to test rendering to the target remoteUrl.

    >>> qux_link = folder[folder.invokeFactory(
    ...     type_name='Link', id='qux-link-title',
    ...     title='Qux Link Title', remoteUrl='http://foo.com')]
    >>> z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
    >>> layer['portal'].portal_workflow.doActionFor(
    ...     qux_link, 'publish')
    >>> testing.logout()

Allow anonymous users to view the by-line.

    >>> from Products.CMFCore.utils import getToolByName
    >>> getToolByName(portal, 'portal_properties'
    ...               ).site_properties.manage_changeProperties(
    ...                   allowAnonymousViewAbout=True)

    >>> import transaction
    >>> transaction.commit()

The author by-lines, descriptions, and event details are included as
with the folder_listing template.

    >>> owner_browser.getLink('Log out').click()
    >>> owner_browser.open(folder.absolute_url())
    >>> print owner_browser.contents
    <...
          <span>Foo Collection Listing Portlet Title</span>
    ...
        href="http://foo.com"
    ...
    >>> print owner_browser.contents
    <...
          <span>Foo Collection Listing Portlet Title</span>
    ...
                <dt class="vevent">
                            <span class="summary">
    ...
                                <a href="http://nohost/plone/Members/test_user_1_/baz-event-title" class="contenttype-event state-published url">Baz Event Title</a>
                            </span>
                            <span class="documentByLine">
                                <span>...<abbr class="dtstart" title="...">...</abbr>...</span>
                                    &mdash;
                                      <span>...by...bar_creator_id...</span>
                            </span>
                        </dt>
                        <dd>
                            <span class="description">blah blah</span> 
                        </dd>
    ...

Link items render links to the remoteUrl.

    >>> owner_browser.getLink('Qux Link Title', index=1)
    <Link text='...Qux Link Title' url='http://foo.com'>

The navigation portlet has also been overridden with one which supports
linking directly to the remoteUrl.

    >>> testing.login(portal, testing.TEST_USER_NAME)
    >>> manager = folder.restrictedTraverse(
    ...     '++contextportlets++plone.leftcolumn')
    >>> from plone.app.portlets.portlets import navigation
    >>> assignment = navigation.Assignment()
    >>> manager['navigation'] = assignment
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

    >>> owner_browser.open(folder.absolute_url())
    >>> from Products.CMFPlone.utils import getFSVersionTuple
    >>> BBB = getFSVersionTuple()[0] < 4
    >>> if BBB:
    ...     owner_browser.getLink('Qux Link Title', index=0)
    ... else:
    ...     owner_browser.getLink('Qux Link Title', index=1)
    <Link text='...Qux Link Title' url='http://foo.com'>
    >>> owner_browser.getLink('Qux Link Title', index=2)
    <Link text='...Qux Link Title' url='http://foo.com'>
