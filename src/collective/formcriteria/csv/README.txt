.. -*-doctest-*-

CSV Export
==========

The data accessed in tabular form from collections is often exactly
the data site admins want to export into other formats such as CSV.
This package provides views for exporting the current query's
collection data into various formats.  The CSV columns are taken from
the collections 'Table Columns' field on the edit tab/form regardless
of whether the table layout is used.  The CSV export link is available
as a document action like the print and send-to actions.

Change the columns and link columns.

    >>> self.loginAsPortalOwner()
    >>> foo_topic = self.folder['foo-topic-title']
    >>> columns = foo_topic.columns
    >>> columns.manage_delObjects(
    ...     ['ModificationDate-column', 'get_size-column',
    ...      'review_state-column'])
    >>> columns['getPath-column'].update(filter='')
    >>> columns['Title-column'].update(link=False, sort='')
    >>> desc_column = columns[columns.invokeFactory(
    ...     type_name='TopicColumn', id='Description-column',
    ...     link=True)]
    >>> foo_topic.manage_delObjects(
    ...     ['crit__sortable_title_FormSortCriterion',
    ...      'crit__get_size_FormSortCriterion',
    ...      'crit__modified_FormSortCriterion',
    ...      'crit__review_state_FormSortCriterion'])
    >>> self.logout()

Add some criteria to the collection.

    >>> _ = foo_topic.addCriterion(
    ...     'path', 'FormRelativePathCriterion')
    >>> foo_topic.addCriterion(
    ...     'Type', 'FormSelectionCriterion'
    ...     ).setValue(['Page', 'Event'])
    >>> foo_topic.getCriterion(
    ...     'SearchableText_FormSimpleStringCriterion'
    ...     ).setFormFields(['value'])
    >>> _ = foo_topic.addCriterion(
    ...     'unsorted', 'FormSortCriterion')
    >>> _ = foo_topic.addCriterion(
    ...     'effective', 'FormSortCriterion')

Open a browser and log in as a normal user.

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

The export link is now available.  Download the raw, un-queried
collection results.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Export').click()
    >>> browser.isHtml
    False
    >>> print browser.headers
    Status: 200 ...
    Content-Disposition: attachment...
    Content-Type: text/csv...

Since the testbrowser can't handle file downloads, we'll check the CSV
output by calling the browser view directly.

    >>> print browser.contents
    Status: 200 OK...
    Content-Type: text/csv
    Content-Disposition: attachment;filename=foo-topic-title.csv
    URL,Title,Description
    http://nohost/plone/Members/test_user_1_/foo-event-title,Foo Event Title,
    http://nohost/plone/Members/test_user_1_/bar-document-title,Bar Document Title,blah
    http://nohost/plone/Members/test_user_1_/baz-event-title,Baz Event Title,blah blah

Add the search form portlet.

    >>> from zope import component
    >>> from plone.i18n.normalizer import (
    ...     interfaces as normalizer_ifaces)
    >>> from collective.formcriteria.portlet import portlet
    >>> self.login()
    >>> manager = foo_topic.restrictedTraverse(
    ...     '++contextportlets++plone.rightcolumn')
    >>> site_path_len = len(portal.getPhysicalPath())
    >>> assignment = portlet.Assignment(
    ...     header='Foo Search Form Title',
    ...     target_collection='/'.join(
    ...         foo_topic.getPhysicalPath()[site_path_len:]))
    >>> name = component.getUtility(
    ...     normalizer_ifaces.IIDNormalizer).normalize(
    ...         assignment.title)
    >>> manager[name] = assignment
    >>> self.logout()

Submit a query.  The exported CSV reflects the user submitted query
and is sorted by relevance.

    >>> browser.open(foo_topic.absolute_url())
    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl('Search Text').value = 'blah'
    >>> form.getControl(name='submit').click()

    >>> browser.getLink('Export').click()
    >>> browser.isHtml
    False
    >>> print browser.contents
    Status: 200 OK...
    Content-Type: text/csv
    Content-Disposition: attachment;filename=foo-topic-title.csv
    URL,Title,Description
    http://nohost/plone/Members/test_user_1_/baz-event-title,Baz Event Title,blah blah
    http://nohost/plone/Members/test_user_1_/bar-document-title,Bar Document Title,blah

Select another sort, The exported CSV reflects the user selected sort
and query.

    >>> browser.open(foo_topic.absolute_url())
    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl('Search Text').value = 'blah'
    >>> form.getControl(name='submit').click()
    >>> browser.getControl(
    ...     name="crit__effective_FormSortCriterion:boolean").click()

    >>> browser.getLink('Export').click()
    >>> browser.isHtml
    False
    >>> print browser.contents
    Status: 200 OK...
    Content-Type: text/csv
    Content-Disposition: attachment;filename=foo-topic-title.csv
    URL,Title,Description
    http://nohost/plone/Members/test_user_1_/bar-document-title,Bar Document Title,blah
    http://nohost/plone/Members/test_user_1_/baz-event-title,Baz Event Title,blah blah

It is also possible to change the CSV format by passing in request
keys with a special 'csv.fmtparam-' prefix.  These values are passed
into Python's csv.writer() factory as keyword arguments.  For example,
to use a tab character as a delimiter instead of ",", add a
'csv.fmtparam-delimiter' key to the request.

    >>> browser.open(foo_topic.absolute_url())
    >>> export_url = browser.getLink('Export').url
    >>> browser.open(export_url+'&csv.fmtparam-delimiter=%09')
    >>> browser.isHtml
    False
    >>> print browser.contents
    Status: 200 OK...
    Content-Type: text/csv
    Content-Disposition: attachment;filename=foo-topic-title.csv
    URL	Title	Description
    http://nohost/plone/Members/test_user_1_/foo-event-title	Foo Event Title	
    http://nohost/plone/Members/test_user_1_/bar-document-title	Bar Document Title	blah
    http://nohost/plone/Members/test_user_1_/baz-event-title	Baz Event Title	blah blah

The export link isn't available if there are no collection columns.

    >>> self.loginAsPortalOwner()
    >>> foo_topic.manage_delObjects(['columns'])
    >>> self.logout()

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Export')
    Traceback (most recent call last):
    LinkNotFoundError
