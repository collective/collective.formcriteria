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

    >>> from plone.app import testing
    >>> from Products.CMFCore.utils import getToolByName
    >>> portal = layer['portal']
    >>> membership = getToolByName(portal, 'portal_membership')
    >>> folder = membership.getHomeFolder(testing.TEST_USER_ID)
    >>> foo_topic = folder['foo-topic-title']
    >>> crit = foo_topic.getCriterion(
    ...     'SearchableText_FormSimpleStringCriterion')
    >>> crit.setValue('bar')
    >>> crit.setFormFields(['value'])
    >>> sort = foo_topic.addCriterion(
    ...     'getPhysicalPath', 'FormSortCriterion')

    >>> import transaction
    >>> transaction.commit()

Open a browser and log in as a user who can change the display layout
for the topic.

    >>> from plone.testing import z2
    >>> browser = z2.Browser(layer['app'])
    >>> browser.handleErrors = False
    >>> browser.open(portal.absolute_url())
    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = testing.TEST_USER_NAME
    >>> browser.getControl(
    ...     'Password').value = testing.TEST_USER_PASSWORD
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
    ...State...

The order column is not included since order is determined by the
collection and is fixed.

    >>> 'Order' in browser.contents
    False

The topic contents are listed in the contents table form and the
titles are links to the item.

    >>> print browser.contents
    <...
    ...Bar Document Title...
    ...2.9 kB...
    ...<span class="state-published">Published</span>...
    >>> from collective.formcriteria.testing import CONTENT_FIXTURE
    >>> now = CONTENT_FIXTURE.now
    >>> str(portal.restrictedTraverse('@@plone').toLocalizedTime(now)
    ...     ) in browser.contents
    True

    >>> browser.getControl('Bar Document Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/bar-document-title'
    selected=False>
    >>> browser.getLink('Bar Document Title')
    <Link text='Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>

The first sort criterion is the default sort.

    >>> browser.getControl(name="sort_on").value
    'sortable_title'

Select different collection columns and which columns link to the
result item.

    >>> z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
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
    ...      'crit__get_size_FormSimpleIntCriterion',
    ...      'crit__modified_FormSortCriterion',
    ...      'crit__modified_FormDateCriterion',
    ...      'crit__review_state_FormSortCriterion',
    ...      'crit__review_state_FormSelectionCriterion'])
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

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
    >>> '2.9 kB' in browser.contents
    False
    >>> now.ISO() in browser.contents
    False
    >>> '<span class="state-published">Published</span>' in browser.contents
    False

The link columns have also been changed.

    >>> browser.getControl('Bar Document Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/bar-document-title'
    selected=False>
    >>> browser.getLink('blah')
    <Link text='blah'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink((now-2).ISO())
    <Link text='...'
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

Query Criteria
--------------

If the query criteria have been assigned to a specific column, the
will be rendered in the filter table header row.  Otherwise they will
be rendered in the search form as usual.

Add the portlet.

    >>> from zope import component
    >>> from plone.i18n.normalizer import (
    ...     interfaces as normalizer_ifaces)
    >>> from collective.formcriteria.portlet import portlet
    >>> testing.login(portal, testing.TEST_USER_NAME)
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
    >>> testing.logout()

If query criteria are configured for the table columns, a filter table
head row will be rendered as a search form.

    >>> foo_topic.setFormLayout('folder_contents')

    >>> import transaction
    >>> transaction.commit()

    >>> browser.open(foo_topic.absolute_url())
    >>> contents_form = browser.getForm(name="folderContentsForm")
    >>> contents_form.getControl(
    ...     name='form_crit__SearchableText_FormSimpleStringCriterion'
    ...     '_value', index=0)
    <Control
    name='form_crit__SearchableText_FormSimpleStringCriterion_value'
    type='text'>
    >>> contents_form.getControl(
    ...     name='form_crit__Title_FormSimpleStringCriterion_value',
    ...     index=0)
    <Control
    name='form_crit__Title_FormSimpleStringCriterion_value'
    type='text'>
    >>> contents_form.getControl('Filter', index=0)
    <SubmitControl name='filter' type='submit'>

Since all query criteria are used in the table columns, no portlet
search form is rendered.

    >>> browser.getForm(name="formcriteria_search")
    Traceback (most recent call last):
    LookupError

The contents view reflects user criteria submitted through the
contents form.

    >>> contents_form.getControl(
    ...     name='form_crit__SearchableText_FormSimpleStringCriterion'
    ...     '_value', index=0).value = 'baz'
    >>> contents_form.getControl('Filter', index=0).click()
    >>> browser.getControl('Bar Document Title')
    Traceback (most recent call last):
    LookupError: label 'Bar Document Title'
    >>> browser.getControl('Baz Event Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/baz-event-title'
    selected=False>

The filter collapsible doesn't collapse when clicking on the search
text box.

    >>> import re
    >>> regexp = re.compile('http://.*?collapsiblesections.css')
    >>> regexp.search(browser.contents).group()
    'http://nohost/plone/portal_css/Plone%20Default/collapsiblesections.css'
    >>> browser.open(portal.absolute_url() + '/collapsiblesections.css')
    >>> print browser.contents
    /*...
    #foldercontents-getPath-filter .collapsibleHeader {
    ...

The search form is rendered if query criteria are present which are
not assigned to a column.

    >>> z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
    >>> columns['getPath-column'].update(filter='')
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

    >>> browser.open(foo_topic.absolute_url())
    >>> portlet_form = browser.getForm(name="formcriteria_search")

The contents view also reflects user criteria submitted through the
portlet form.

    >>> portlet_form.getControl(
    ...     name='form_crit__SearchableText_FormSimpleStringCriterion'
    ...     '_value').value = 'baz'
    >>> portlet_form.getControl(name='submit').click()
    >>> browser.getControl('Bar Document Title')
    Traceback (most recent call last):
    LookupError: label 'Bar Document Title'
    >>> browser.getControl('Baz Event Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/baz-event-title'
    selected=False>

If no query criteria are configured, the filter table head row will
not be rendered.

    >>> z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
    >>> columns['Title-column'].update(filter='')
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

    >>> browser.open(foo_topic.absolute_url())
    >>> print browser.contents
    <...
          <thead...
            <tr>
                <th class="nosort"...>&#160;</th>
                <th class="nosort sortColumn"
                    id="foldercontents-sortable_title-column">
                      &#160;
                      Title
                      &#160;
                    </th>
                <th class="nosort noSortColumn"
                    id="foldercontents-Description-column">
                      &#160;
                      Description
                      &#160;
                    </th>
                <th class="nosort noSortColumn"
                    id="foldercontents-EffectiveDate-column">
                      &#160;
                      Effective Date
                      &#160;
                    </th>
            </tr>
          </thead...
          <tbody...

Cells that link to the item have just a link and no icon.  If the
special "Path" column is include, it will display an icon.

    >>> print browser.contents
    <...
                  <td class="notDraggable">
                      <input type="checkbox" class="noborder" name="paths:list" id="cb_-plone-Members-test_user_1_-bar-document-title" value="/plone/Members/test_user_1_/bar-document-title" alt="Select Bar Document Title" title="Select Bar Document Title" />
                      <input type="hidden" name="selected_obj_paths:list" value="/plone/Members/test_user_1_/bar-document-title" />
                      <label for="cb_-plone-Members-test_user_1_-bar-document-title">
                        <span class="contenttype-document">
    ...
                        </span>
                        <span class="hiddenStructure">Bar Document Title</span>
                      </label>
                  </td>
    ...
                        <span class="contenttype-document">
                          <a href="http://nohost/plone/Members/test_user_1_/bar-document-title"...
                            blah
                          </a>
                        </span>
    ...
