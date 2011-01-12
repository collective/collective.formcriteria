.. -*-doctest-*-

Table Columns
=============

Table columns, much like query and sort criteria, are represented by
objects contained within the collection.  These column objects allow
rich, spreadsheet like, functionality.  Each column objects controls:

  - the metadata field displayed in each column
  - which columns link to the result item
  - the expression used to render the metadata field
  - an optional sort criterion when the column header is clicked
  - an optional query criterion for column filtering

When a topic is created using the template included in the
'profile-collective.formcriteria:formcriteria-columns', it has a
columns container.

    >>> foo_topic = self.folder['foo-topic-title']
    >>> foo_topic.columns
    <TopicColumns at
    /plone/Members/test_user_1_/foo-topic-title/columns>

The columns container starts with column objects representing the
default folder contents table columns.  Note that a colun object is
also used to represent the checkbox column for performing actions on
the selected items.

    >>> import pprint
    >>> foo_topic.columns.contentValues()
    [<TopicColumn at
      /plone/Members/test_user_1_/foo-topic-title/columns/getPath-column>,
     <TopicColumn at
      /plone/Members/test_user_1_/foo-topic-title/columns/Title-column>,
     <TopicColumn at
      /plone/Members/test_user_1_/foo-topic-title/columns/get_size-column>,
     <TopicColumn at
      /plone/Members/test_user_1_/foo-topic-title/columns/ModificationDate-column>,
     <TopicColumn at
      /plone/Members/test_user_1_/foo-topic-title/columns/review_state-column>]

    >>> from collective.formcriteria.columns import content
    >>> for column in foo_topic.columns.contentValues():
    ...     pprint.pprint([
    ...         (field.getName(), field.getAccessor(column)())
    ...         for field in content.column_schema.fields()])
    [('id', 'getPath-column'),
     ('link', False),
     ('sum', False),
     ('expression', ''),
     ('sort', ''),
     ('filter', 'crit__SearchableText_FormSimpleStringCriterion')]
    [('id', 'Title-column'),
     ('link', True),
     ('sum', False),
     ('expression', ''),
     ('sort', 'crit__sortable_title_FormSortCriterion'),
     ('filter', 'crit__Title_FormSimpleStringCriterion')]
    [('id', 'get_size-column'),
     ('link', False),
     ('sum', False),
     ('expression',
      "python:modules['collective.formcriteria.columns.utils'].format_number(value)"),
     ('sort', 'crit__get_size_FormSortCriterion'),
     ('filter', 'crit__get_size_FormSimpleIntCriterion')]
    [('id', 'ModificationDate-column'),
     ('link', False),
     ('sum', False),
     ('expression', ''),
     ('sort', 'crit__modified_FormSortCriterion'),
     ('filter', 'crit__modified_FormDateCriterion')]
    [('id', 'review_state-column'),
     ('link', False),
     ('sum', False),
     ('expression',
      'python:portal.portal_workflow.getTitleForStateOnType(value, item.Type)'),
     ('sort', 'crit__review_state_FormSortCriterion'),
     ('filter', 'crit__review_state_FormSelectionCriterion')]

Open a browser and log in as a user who can make changes to the
topic.

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

Since columns are managed in the columns container, the "Table
Columns" field and related fields are not included on the topic edit
form.

    >>> browser.open(foo_topic.absolute_url()+'/edit')
    >>> browser.getControl('Table Columns')
    Traceback (most recent call last):
    LookupError: label 'Table Columns'
    >>> browser.getControl('Table Column Links')
    Traceback (most recent call last):
    LookupError: label 'Table Column Links'
    >>> browser.getControl('Table Column Sums')
    Traceback (most recent call last):
    LookupError: label 'Table Column Sums'

Column order can be managed through the browser.

    >>> browser.getLink('Columns').click()
    >>> print browser.contents
    <...
    <tr class="draggable odd"
    id="folder-contents-item-getPath-column">
    ...

Columns can be added through the browser.

    >>> browser.getLink('Topic Column').click()
    >>> browser.getControl('Field').getControl(
    ...     'Creation Date').selected = True
    >>> browser.getControl('Sort Criterion').getControl(
    ...     'Modification Date').selected = True
    >>> browser.getControl('Filter Criterion').getControl(
    ...     'Modification Date').selected = True
    >>> browser.getControl('Save').click()
    >>> print browser.contents
    <...
    ...Changes saved...

When managing the columns tabs are available for editing the
collection, managing the criteria, and returning to view the topic.

    >>> TODO

The tabs when managing a column are sensible and behave properly.
Tabs are also available for editing the collection, managing the
criteria, and returning to view the topic.

    >>> TODO

A user is prompted to log in when directly accessing a column's edit link.

    >>> TODO