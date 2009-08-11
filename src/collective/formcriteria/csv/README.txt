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

Add some criteria to the collection.

    >>> foo_topic = self.folder['foo-topic-title']
    >>> _ = foo_topic.addCriterion(
    ...     'path', 'FormRelativePathCriterion')
    >>> foo_topic.addCriterion(
    ...     'Type', 'FormSelectionCriterion'
    ...     ).setValue(['Page', 'Event'])
    >>> foo_topic.addCriterion(
    ...     'SearchableText','FormSimpleStringCriterion'
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

The export link isn't available if the 'Table Columns' field is not
set.

    >>> foo_topic.update(customViewFields=[])
    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Export')
    Traceback (most recent call last):
    LinkNotFoundError

Add some columns to the 'Table Columns' field.

    >>> foo_topic.update(customViewFields=['Title', 'Description'])

The export link is now available.  Download the raw, un-queried
collection results.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Export').click()
    >>> browser.isHtml
    False
    >>> print browser.headers
    Status: 200 OK...
    Content-Disposition: attachment...
    Content-Type: text/csv...

Since the testbrowser can't handle file downloads, we'll check the CSV
output by calling the browser view directly.

    >>> print browser.contents
    Status: 200 OK...
    Content-Type: text/csv
    Content-Disposition: attachment;filename=foo-topic-title.csv
    Title,Description
    Foo Event Title,
    Bar Document Title,blah
    Baz Event Title,blah blah

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
    Title,Description
    Baz Event Title,blah blah
    Bar Document Title,blah

Select another sort, The exported CSV reflects the user selected sort
and query.

    >>> browser.open(foo_topic.absolute_url())
    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl('Search Text').value = 'blah'
    >>> form.getControl(name='submit').click()
    >>> browser.getLink('Effective Date').click()

    >>> browser.getLink('Export').click()
    >>> browser.isHtml
    False
    >>> print browser.contents
    Status: 200 OK...
    Content-Type: text/csv
    Content-Disposition: attachment;filename=foo-topic-title.csv
    Title,Description
    Bar Document Title,blah
    Baz Event Title,blah blah

