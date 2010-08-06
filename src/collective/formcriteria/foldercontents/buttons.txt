.. -*-doctest-*-

Folder Contents Buttons
-----------------------

The folder contents buttons are also usable on collections.

Remove the sort criteria.

    >>> self.loginAsPortalOwner()
    >>> foo_topic = self.folder['foo-topic-title']
    >>> columns = foo_topic.columns
    >>> columns['Title-column'].update(sort='')
    >>> columns['get_size-column'].update(sort='')
    >>> columns['ModificationDate-column'].update(sort='')
    >>> columns['review_state-column'].update(sort='')
    >>> foo_topic.manage_delObjects(
    ...     ['crit__sortable_title_FormSortCriterion',
    ...      'crit__get_size_FormSortCriterion',
    ...      'crit__modified_FormSortCriterion',
    ...      'crit__review_state_FormSortCriterion'])
    >>> portal.portal_workflow.doActionFor(foo_topic, 'publish')
    >>> self.logout()

Create a folder and move one item into the folder.

    >>> self.login()
    >>> foo_folder = folder[folder.invokeFactory(
    ...     type_name='Folder', id='foo-folder-title',
    ...     title='Foo Folder Title')]
    >>> foo_folder.manage_pasteObjects(
    ...     folder.manage_cutObjects(['bar-document-title']))
    [{'new_id': 'bar-document-title', 'id': 'bar-document-title'}]
    >>> self.logout()

Open a browser and log in as a user who can use the folder contents
buttons on the content listed.

    >>> from Products.Five.testbrowser import Browser
    >>> from Products.PloneTestCase import ptc
    >>> browser = Browser()
    >>> browser.handleErrors = False
    >>> browser.open(portal.absolute_url())
    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = ptc.default_user
    >>> browser.getControl(
    ...     'Password').value = ptc.default_password
    >>> browser.getControl('Log in').click()

Both copies appear in the collection.

    >>> foo_topic = self.folder['foo-topic-title']
    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Baz Event Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/baz-event-title'
    selected=False>
    >>> browser.getControl('Bar Document Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/foo-folder-title/bar-document-title'
    selected=False>

Select both and click the "Copy" button.

    >>> browser.getControl('Baz Event Title').selected = True
    >>> browser.getControl('Bar Document Title').selected = True
    >>> browser.getControl('Copy').click()

The "Paste" button is not available for the collection.

    >>> browser.getControl('Paste')
    Traceback (most recent call last):
    LookupError: label 'Paste'

Paste the copied items into the folder.

    >>> browser.open(foo_folder.absolute_url()+'/folder_contents')
    >>> browser.getControl('Paste').click()
    >>> print browser.contents
    <...
    ...Item(s) pasted...
    >>> sorted(folder.contentIds())
    ['baz-event-title', 'foo-event-title', 'foo-folder-title',
    'foo-topic-title']
    >>> sorted(foo_folder.contentIds())
    ['bar-document-title', 'baz-event-title',
    'copy_of_bar-document-title']

Use the collection again to select two items, one in each folder and
click the "Cut" button.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl(
    ...     'Baz Event Title', index=0).selected = True
    >>> browser.getControl(
    ...     'Bar Document Title', index=0).selected = True
    >>> browser.getControl('Cut').click()

Paste the cut items into another folder.

    >>> browser.open(folder.absolute_url()+'/folder_contents')
    >>> browser.getControl('Paste').click()
    >>> print browser.contents
    <...
    ...Item(s) pasted...
    >>> sorted(folder.contentIds())
    ['bar-document-title', 'baz-event-title', 'foo-event-title',
    'foo-folder-title', 'foo-topic-title']
    >>> sorted(foo_folder.contentIds())
    ['baz-event-title', 'copy_of_bar-document-title']

Use the collection again to select two items, one in each folder and
click the "Rename" button.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl(
    ...     'Baz Event Title', index=0).selected = True
    >>> browser.getControl(
    ...     'Bar Document Title', index=1).selected = True
    >>> browser.getControl('Rename').click()

Rename the selected items.

    >>> browser.getControl('New Short Name', index=0).value
    'baz-event-title'
    >>> browser.getControl(
    ...     'New Short Name', index=0).value = 'qux-event-title'
    >>> browser.getControl('New Title', index=0).value
    'Baz Event Title'
    >>> browser.getControl(
    ...     'New Title', index=0).value = 'Qux Event Title'

    >>> browser.getControl('New Short Name', index=1).value
    'copy_of_bar-document-title'
    >>> browser.getControl(
    ...     'New Short Name', index=1).value = 'qux-document-title'
    >>> browser.getControl('New Title', index=1).value
    'Bar Document Title'
    >>> browser.getControl(
    ...     'New Title', index=1).value = 'Qux Document Title'

    >>> browser.getControl('Rename All').click()
    >>> print browser.contents
    <...
    ...2 item(s) renamed...
    >>> sorted(folder.contentIds())
    ['bar-document-title', 'foo-event-title', 'foo-folder-title',
    'foo-topic-title', 'qux-event-title']
    >>> sorted(foo_folder.contentIds())
    ['baz-event-title', 'qux-document-title']
    >>> folder['qux-event-title'].Title()
    'Qux Event Title'
    >>> folder['foo-folder-title']['qux-document-title'].Title()
    'Qux Document Title'

Use the collection again to select two items, one in each folder and
click the "Change State" button.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Qux Event Title').selected = True
    >>> browser.getControl('Qux Document Title').selected = True
    >>> browser.getControl('Change State').click()

Change the state of the selected items.

    >>> browser.getControl('Retract').selected = True
    >>> browser.getControl('Save').click()
    >>> print browser.contents
    <...
    ...Item state changed...
    >>> sorted(folder.contentIds())
    ['bar-document-title', 'foo-event-title', 'foo-folder-title',
    'foo-topic-title', 'qux-event-title']
    >>> sorted(foo_folder.contentIds())
    ['baz-event-title', 'qux-document-title']
    >>> portal.portal_workflow.getInfoFor(
    ...     folder['qux-event-title'], 'review_state')
    'private'
    >>> portal.portal_workflow.getInfoFor(
    ...     folder['foo-folder-title']['qux-document-title'],
    ...     'review_state')
    'private'

Use the collection again to select two items, one in each folder and
click the "Delete" button.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Qux Event Title').selected = True
    >>> browser.getControl('Qux Document Title').selected = True
    >>> browser.getControl('Delete').click()
    >>> print browser.contents
    <...
    ...Item(s) deleted...

The items have been deleted from their respective containers.

    >>> sorted(folder.contentIds())
    ['bar-document-title', 'foo-event-title', 'foo-folder-title',
    'foo-topic-title']
    >>> sorted(foo_folder.contentIds())
    ['baz-event-title']

If no buttons are available, then the checkboxes are not rendered.

Remove the copy permission for anonymous users to that the copy and
rename buttons aren't available.

    >>> portal.manage_permission(
    ...     'Copy or Move', roles=['Authenticated', 'Manager'],
    ...     acquire=0)

Open a browser and visit the topic anonymously.  If anonymous has the
"List folder contents" permission, the folder_contents table is
viewable.

    >>> foo_topic.manage_permission(
    ...     'List folder contents', roles=['Anonymous', 'Manager'],
    ...     acquire=1)

    >>> anon_browser = Browser()
    >>> anon_browser.handleErrors = False
    >>> anon_browser.open(foo_topic.absolute_url())

The checkboxes are no longer available.

    >>> anon_browser.getControl('Bar Document Title')
    Traceback (most recent call last):
    LookupError: label 'Bar Document Title'
    >>> anon_browser.getLink('All')
    Traceback (most recent call last):
    LinkNotFoundError
