.. -*-doctest-*-

Contents View
=============

A version of the folder_contents can be used with collections
where the columns are those specified in the collection's "Table
Columns" field.  The buttons at the bottom of the folder contents view
will then be applied to the selected items.

Any columns that are selected in the collection's "Table
Columns" field that are also selected in the "Table Column Links"
field will be rendered as links.  Note that it's possible to select a
link column that isn't a table column which will have no effect.

Add a simple string criterion for the SearchableText index on the
criteria tab.  Set a default search term.  Add a sort criteria for
consistent ordering.

    >>> foo_topic = self.folder['foo-topic-title']
    >>> crit = foo_topic.getCriterion(
    ...     'SearchableText_FormSimpleStringCriterion')
    >>> crit.setValue('bar')
    >>> crit.setFormFields(['value'])
    >>> sort = foo_topic.addCriterion(
    ...     'getPhysicalPath', 'FormSortCriterion')

Open a browser and log in as a user who can change the display layout
for the topic.

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

Change the topic's display layout and the search form results layout
to the contents view.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Tabular Form').click()
    >>> print browser.contents
    <...
    ...View changed...

The view renders the contents form with the default columns.

    >>> browser.getForm(name="folderContentsForm")
    <zope.testbrowser.browser.Form object at ...>
    >>> print browser.contents
    <...
    ...Title...
    ...Size...
    ...Modification Date...
    ...&#160;State&#160;...

The order column is not included since order is determined by the
collection and is fixed.

    >>> 'Order' in browser.contents
    False

The topic contents are listed in the contents table form and the
titles are links to the item.

    >>> print browser.contents
    <...
    ...Bar Document Title...
    ...3000...
    ...2009-01-15...
    ...<span class="state-published">published</span>...

    >>> browser.getControl('Bar Document Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/bar-document-title'
    selected=False>
    >>> browser.getLink('Bar Document Title')
    <Link text='Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>

Select different collection columns and which columns link to the
result item.

    >>> self.loginAsPortalOwner()
    >>> columns = foo_topic.columns
    >>> columns.manage_delObjects(
    ...     ['ModificationDate-column', 'get_size-column',
    ...      'review_state-column'])
    >>> columns['Title-column'].update(link=False)
    >>> desc_column = columns[columns.invokeFactory(
    ...     type_name='TopicColumn', id='Description-column',
    ...     link=True)]
    >>> effective_column = columns[columns.invokeFactory(
    ...     type_name='TopicColumn', id='EffectiveDate-column',
    ...     link=True)]
    >>> foo_topic.manage_delObjects(
    ...     ['crit__get_size_FormSortCriterion',
    ...      'crit__modified_FormSortCriterion',
    ...      'crit__review_state_FormSortCriterion'])
    >>> self.logout()

The view renders the contents form with the specified columns.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getForm(name="folderContentsForm")
    <zope.testbrowser.browser.Form object at ...>
    >>> print browser.contents
    <...
    ...Description...
    ...Effective Date...
    ...Title...
    >>> 'Size' in browser.contents
    False
    >>> 'Modification Date' in browser.contents
    False
    >>> '&#160;State&#160;' in browser.contents
    False

The topic contents are also listed with the specified columns.

    >>> print browser.contents
    <...
    ...Bar Document Title...
    ...blah...
    ...2009-01-13...
    >>> '0 kB' in browser.contents
    False
    >>> '2009-01-15' in browser.contents
    False
    >>> '<span class="state-published">published</span>' in browser.contents
    False

The link columns have also been changed.

    >>> browser.getControl('Bar Document Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/bar-document-title'
    selected=False>
    >>> browser.getLink('blah')
    <Link text='blah'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('2009-01-13')
    <Link text='2009-01-13 01:00:00'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError

The item selection header row reflects the new number of columns.

    >>> print browser.contents
    <...
    ...<thead>...
    ...<th colspan="4"...
    ...</thead>...

The KSS update table view also reflects the selected columns.

    >>> browser.open(
    ...     foo_topic.absolute_url()+'/foldercontents_update_table')
    >>> print browser.contents
    <...
    ...Description...
    ...Effective Date...
    ...Title...
    >>> 'Size' in browser.contents
    False
    >>> 'Modification Date' in browser.contents
    False
    >>> '&#160;State&#160;' in browser.contents
    False

Search Form Portlet
-------------------

Add the portlet.

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

The search form is also rendered if form criteria are present.

    >>> foo_topic.setFormLayout('folder_contents')
    >>> browser.open(foo_topic.absolute_url())
    >>> form = browser.getForm(name="formcriteria_search")

The contents view also reflects user submitted criteria.

    >>> form.getControl(
    ...     name='form_crit__SearchableText_FormSimpleStringCriterion'
    ...     '_value').value = 'baz'
    >>> form.getControl(name='submit').click()
    >>> browser.getControl('Bar Document Title')
    Traceback (most recent call last):
    LookupError: label 'Bar Document Title'
    >>> browser.getControl('Baz Event Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/baz-event-title'
    selected=False>
