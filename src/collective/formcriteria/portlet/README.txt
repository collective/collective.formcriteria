.. -*-doctest-*-

==================
Collection Portlet
==================

The collection portlet included with collective.formcriteria uses
Plone's folder_listing template to render the contents.  This provides
a richer available data structure including descriptions, event
handling, author information, etc..

Add a criterion to the topic.

    >>> foo_topic = self.folder['foo-topic-title']
    >>> path_crit = foo_topic.addCriterion(
    ...     'path', 'FormRelativePathCriterion')
    >>> path_crit.setRecurse(True)

Chang the folder layout to be something other than the folder_listing
template to differentiate output.

    >>> folder.setLayout('folder_summary_view')

Login as a user that can manage portlets.

    >>> from Products.Five.testbrowser import Browser
    >>> from Products.PloneTestCase import ptc
    >>> owner_browser = Browser()
    >>> owner_browser.handleErrors = False
    >>> owner_browser.open(portal.absolute_url())
    >>> owner_browser.getLink('Log in').click()
    >>> owner_browser.getControl(
    ...     'Login Name').value = ptc.portal_owner
    >>> owner_browser.getControl(
    ...     'Password').value = ptc.default_password
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

    >>> qux_link = self.folder[self.folder.invokeFactory(
    ...     type_name='Link', id='qux-link-title',
    ...     title='Qux Link Title', remoteUrl='http://foo.com')]
    >>> self.loginAsPortalOwner()
    >>> self.portal.portal_workflow.doActionFor(
    ...     qux_link, 'publish')
    >>> self.logout()

Allow anonymous users to view the by-line.

    >>> from Products.CMFCore.utils import getToolByName
    >>> getToolByName(portal, 'portal_properties'
    ...               ).site_properties.manage_changeProperties(
    ...                   allowAnonymousViewAbout=True)

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
                            <span class="contenttype-event summary">
    ...
                                <a href="http://nohost/plone/Members/test_user_1_/baz-event-title" class="state-published url">Baz Event Title</a>
                            </span>
                            <span class="documentByLine">
                                <span>
                                    (from
                                     <abbr class="dtstart" title="...">...</abbr> to
                                     <abbr class="dtend" title="...">...</abbr>)
                                </span>
                                    &mdash;
                                      <span>
                                        by
                                      ...bar_creator_id...
                                      </span>
                            </span>
                        </dt>
                        <dd>
                            <span class="description">blah blah</span> 
                        </dd>
    ...

Link items render links to the remoteUrl.

    >>> owner_browser.getLink('Qux Link Title', index=1)
    <Link text='Qux Link Title' url='http://foo.com'>

The navigation portlet has also been overridden with one which supports
linking directly to the remoteUrl.

    >>> self.login()
    >>> manager = self.folder.restrictedTraverse(
    ...     '++contextportlets++plone.leftcolumn')
    >>> from plone.app.portlets.portlets import navigation
    >>> assignment = navigation.Assignment()
    >>> manager['navigation'] = assignment
    >>> self.logout()

    >>> owner_browser.open(folder.absolute_url())
    >>> owner_browser.getLink('Qux Link Title', index=0)
    <Link text='...Qux Link Title' url='http://foo.com'>
