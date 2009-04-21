.. -*-doctest-*-

=======================
collective.formcriteria
=======================

This package extends the Products.ATContentTypes.criteria types to
create a search forms.  Specifically, any criterion fields which are
selected in each criterion's "Form Fields", then those fields will be
rendered on the search form.  The values set on the criteria edit form
become the default values on the search form.  Search terms submitted
through the search form supplement any criteria not on the search
form.  IOW, criteria not appearing on the form become the base query
built into the search form.

A new "Search Form" display layout is provided that renders the search
form and the collection body text but no results.  The search form on
this layout will display results using the layout specified in the
"Form Results Layout" field of the collection's edit form.

The search form can also be rendered in a search form portlet based on
plone.portlet.collection.  The portlet will not render on the search
form view or the criteria edit form but otherwise will render the
search form for the designated collection according to the portlet
settings.

Thus the collection can use either the search form or a results
listing as the display layout.  Users can initiate searches using
either the form or the portlet.  The portlet also reflects any
submitted search terms and thus provides a convenient way for users to
refine their searches.

Multiple sort criteria can also be added that will render user
selectable sort links on the batch macro.  See
collective/formcriteria/criteria/sort.txt for more details.

Also provided is an alternative display layout that uses the folder
contents table.  This layout is not yet fully functional but provides
the basis for some very rich site admin functionality.

WARNING: Uninstall
==================

Uninstalling this product after having added any collections or adding
criteria to any collections, even ones added before install, is
untested and may leave your collections broken.

Form Criteria
=============

Start with a collection and some content for search results.

    >>> from Products.PloneTestCase import ptc
    >>> self.login()
    >>> foo_topic = self.folder['foo-topic-title']
    >>> foo_topic
    <Topic at /plone/Members/test_user_1_/foo-topic-title>
    >>> self.folder['bar-document-title']
    <ATDocument at /plone/Members/test_user_1_/bar-document-title>
    >>> self.folder['baz-event-title']
    <ATEvent at /plone/Members/test_user_1_/baz-event-title>

Create the browser object we'll be using.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.handleErrors = False

Log in as a normal user.

    >>> browser.open(portal.absolute_url())
    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = ptc.default_user
    >>> browser.getControl(
    ...     'Password').value = ptc.default_password
    >>> browser.getControl('Log in').click()

Change the display layout of the collection to the "Search Form".

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Search Form').click()
    >>> print browser.contents
    <...
    ...View changed...

Login as a user that can manage portlets.

    >>> owner_browser = Browser()
    >>> owner_browser.handleErrors = False
    >>> owner_browser.open(portal.absolute_url())
    >>> owner_browser.getLink('Log in').click()
    >>> owner_browser.getControl(
    ...     'Login Name').value = ptc.portal_owner
    >>> owner_browser.getControl(
    ...     'Password').value = ptc.default_password
    >>> owner_browser.getControl('Log in').click()

Add the search form portlet for this collection to the folder.

    >>> owner_browser.open(folder.absolute_url())
    >>> owner_browser.getLink('Manage portlets').click()
    >>> owner_browser.getControl(
    ...     'Search form portlet', index=1).selected = True
    >>> owner_browser.getForm(index=3).submit() # manually w/o JS
    >>> print owner_browser.contents
    <...
    ...Add Search Form Portlet...

    >>> header = owner_browser.getControl('Portlet header')
    >>> header.value = 'Foo Search Form Title'
    >>> foo_topic_path = '/'.join(
    ...     ('',)+ foo_topic.getPhysicalPath()[
    ...         len(portal.getPhysicalPath()):])
    >>> header.mech_form.new_control(
    ...     type='checkbox', name="form.target_collection",
    ...     attrs=dict(checked='checked', value=foo_topic_path))
    >>> owner_browser.getControl('Save').click()
    >>> print owner_browser.contents
    <...
    ...Foo Search Form Title...

Go to the collection's edit tab and set the "Form Results Layout"
field.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl('Collection').selected = True
    >>> browser.getControl('Save').click()
    >>> print browser.contents
    <...
    ...Changes saved...

Go to the "Criteria" tab and add a criterion for the workflow state
that won't appear on the form.  Then set the query term to return only
published content.

    >>> browser.getLink('Criteria').click()
    >>> form = browser.getForm(name='criteria_select')
    >>> form.getControl('State').selected = True
    >>> form.getControl(
    ...     'Select values from list', index=1).selected = True
    >>> form.getControl('Add criteria').click()
    >>> print browser.contents
    <...
    ...State...
    ...Select values from list...

Since the test browser doesn't have JavaScript, test the
discrimination of criteria types by index manually.

    >>> foo_topic.allowedCriteriaForField('review_state')
    ['FormSelectionCriterion', 'FormCheckboxCriterion',
    'FormSimpleStringCriterion', 'FormListCriterion',
    'FormCommaCriterion', 'FormSortCriterion']
    >>> foo_topic.allowedCriteriaForField(
    ...     'review_state', display_list=True)
    <DisplayList
    [('FormSelectionCriterion', 'Select values from list'),
     ('FormCheckboxCriterion', 'Check values'),
     ('FormSimpleStringCriterion', 'Text'),
     ('FormListCriterion', 'List of values'),
     ('FormCommaCriterion', 'Enter comma separated values'),
     ('FormSortCriterion', 'Sort results')] at ...>

Set the query term and save.

    >>> form = browser.getForm(action="criterion_edit_form", index=0)
    >>> form.getControl('published').selected = True
    >>> form.getControl('Save').click()
    >>> print browser.contents
    <...
    ...Changes saved...

Open another browser as an anonymous user.

    >>> anon_browser = Browser()
    >>> anon_browser.handleErrors = False

Before the topic has any form criteria, the search form is not
present.

    >>> anon_browser.open(foo_topic.absolute_url()+'/atct_topic_view')
    >>> anon_browser.getForm(name="formcriteria_search")
    Traceback (most recent call last):
    LookupError

Add a simple string criterion for the SearchableText index on the
criteria tab.

    >>> form = browser.getForm(name='criteria_select')
    >>> form.getControl('Search Text').selected = True
    >>> form.getControl(name="criterion_type").getControl(
    ...     'Text', index=1).selected = True
    >>> form.getControl('Add criteria').click()
    >>> print browser.contents
    <...
    ...Search Text...
    ...A simple string criterion...

Select the criterion's 'value' field as a form field so it will appear
on the search form.

    >>> browser.getControl(
    ...     name='crit__SearchableText_FormSimpleStringCriterion'
    ...     '_formFields:list').getControl('Value').selected = True

Set a default search term.

    >>> browser.getControl(
    ...     name="crit__SearchableText_FormSimpleStringCriterion"
    ...     "_value").value = 'bar'
    >>> browser.getControl(name="form.button.Save").click()
    >>> print browser.contents
    <...
    ...Changes saved...

If no form value have been submitted, such as on a fresh load of the
topic view, the default term will be used in the query returning only
one of the content objects.

    >>> len(foo_topic.queryCatalog())
    1

    >>> anon_browser.open(foo_topic.absolute_url()+'/atct_topic_view')
    >>> anon_browser.getLink('Bar Document Title')
    <Link text='Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> anon_browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError

Now that a form criterion has been added, the search form is
rendered.

    >>> anon_browser.open(foo_topic.absolute_url())
    >>> form = anon_browser.getForm(name="formcriteria_search")
    
Criterion fields that haven't been selected in "Form Fields" don't
appear on the search form.

    >>> form.getControl(
    ...     name='form_crit__SearchableText_FormSimpleStringCriterion'
    ...     '_formFields:list')
    Traceback (most recent call last):
    LookupError: name
    'form_crit__SearchableText_FormSimpleStringCriterion_formFields:list'

The label for the criterion corresponds to the form element for the
first criterion field.

    >>> ctl = form.getControl('Search Text')

Enter a search term and submit the query.  The topic will now list the
other content object.

    >>> ctl.value = 'baz'
    >>> form.getControl(name='submit').click()
    >>> anon_browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> anon_browser.getLink('Baz Event Title')
    <Link text='Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

Since the search form has been submitted, the results are rendered on
the layout specified by the "Form Results Layout".

    >>> anon_browser.url.startswith(
    ...     'http://nohost/plone/Members/test_user_1_/foo-topic-title'
    ...     '/atct_topic_view')
    True

The search form portlet also reflects the search term submitted rather
than the default value submitted on the criteria tab.

    >>> form = anon_browser.getForm(name="formcriteria_search")
    >>> ctl = form.getControl('Search Text')
    >>> ctl.value
    'baz'

If the search form is submitted from this page, the results are still
rendered on the same view.

    >>> ctl.value = 'bar'
    >>> form.getControl(name='submit').click()
    >>> anon_browser.url.startswith(
    ...     'http://nohost/plone/Members/test_user_1_/foo-topic-title'
    ...     '/atct_topic_view')
    True

Values are also ignored if submitted for criteria fields which are not
listed in "Form Fields".

    >>> crit = foo_topic.getCriterion(
    ...     'SearchableText_FormSimpleStringCriterion')
    >>> crit.setFormFields([])
    >>> anon_browser.open(
    ...     foo_topic.absolute_url()+'/atct_topic_view'
    ...     '?form_crit__SearchableText_FormSimpleStringCriterion'
    ...     '_value=baz')
    >>> anon_browser.getLink('Bar Document Title')
    <Link text='Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> anon_browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> crit.setFormFields(['value'])

The search form portlet successfully renders when viewed on a context
other than the portlet.

    >>> anon_browser.open(folder.absolute_url())
    >>> form = anon_browser.getForm(name="formcriteria_search")

Ensure that collective.formcriteria doesn't break existing ATTopic
instances such as those created by default in a Plone site.

    >>> owner_browser.open(portal.news.absolute_url())
    >>> print owner_browser.contents
    <...
    ...Site News...
    ...There are currently no items in this folder...

    >>> owner_browser.getLink('Criteria').click()
    >>> print owner_browser.contents
    <...
    ...Criteria for News...

Contents View
=============

Change the topic's display layout and the search form results layout
to the contents view.

    >>> foo_topic.setFormLayout('folder_contents_view')
    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Tabular Form').click()
    >>> print browser.contents
    <...
    ...View changed...

The view renders the contents form.

    >>> browser.getForm(name="folderContentsForm")
    <zope.testbrowser.browser.Form object at ...>

The topic contents are listed in the contents table form.

    >>> browser.getControl('Bar Document Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/bar-document-title'
    selected=False>
    >>> browser.getControl('Baz Event Title')
    Traceback (most recent call last):
    LookupError: label 'Baz Event Title'

The search form is also rendered if form criteria are present.

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

Make sure none of the collective.formcriteria extensions interfere
with existing ATTopic instances.

    >>> browser.open(portal.events.aggregator.absolute_url())
