.. -*-doctest-*-

=======================
collective.formcriteria
=======================

This package provides extends the Products.ATContentTypes.criteria
types to create a search forms.  If any of the criterion fields are
selected in the criterion's "Form Fields" field, then those fields
will be rendered on the search form.

A new "Search Form" display layout is provided that renders the search
form fully expanded and the collection body text but no results.  When
this layout is used, the search form will display results using the
layout specified in the "Form Results Layout" collection field.
Otherwise the search form always displays results using the layout it
was rendered on and always starts out collapsed.  In this way, the
collection creator can determine whether the collection should have a
default view of just the search form or should use a results listing
as a default view.  Likewise, users of the collection can use any
collection layout to view results and can modify their search terms
easily by expanding the search form.

Users can use the form to submit criteria to supplement any search
criteria in the topic.  Values entered on the criteria tab for the
topic become the default values on the form.

Multiple sort criteria can also be added that will render user
selectable sort links on the batch macro.  See
collective/formcriteria/criteria/sort.txt for more details.

Also provided is an alternative display layout that uses the folder
contents table and can still display the search form viewlet.

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
    ...     'Select values from list').selected = True
    >>> form.getControl('Add criteria').click()
    >>> print browser.contents
    <...
    ...State...
    ...Select values from list...

    >>> form = browser.getForm(action="criterion_edit_form", index=0)
    >>> form.getControl('published').selected = True
    >>> form.getControl('Save').click()
    >>> print browser.contents
    <...
    ...Changes saved...

Open another browser as an anymous user.

    >>> anon_browser = Browser()
    >>> anon_browser.handleErrors = False

Before the topic has any form criteria, the serach form is not
present.

    >>> anon_browser.open(foo_topic.absolute_url())
    >>> anon_browser.getForm(name="formcriteria_search")
    Traceback (most recent call last):
    LookupError

Add a simple string criterion for searchable text on the criteria tab.

    >>> form = browser.getForm(name='criteria_select')
    >>> form.getControl('Search Text').selected = True
    >>> form.getControl(name="criterion_type").getControl(
    ...     'Text').selected = True
    >>> form.getControl('Add criteria').click()
    >>> print browser.contents
    <...
    ...Search Text...
    ...A simple string criterion...

Select the criterion's 'value' field as a form field so it will appear
on the search form.

    >>> browser.getControl(
    ...     name='crit__SearchableText_ATSimpleStringCriterion'
    ...     '_formFields:list').getControl('Value').selected = True

Set a default search term.

    >>> browser.getControl(
    ...     name="crit__SearchableText_ATSimpleStringCriterion"
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

Now that a form criterion has been added, the topic view displays the
search form.

    >>> form = anon_browser.getForm(name="formcriteria_search")

Since the "Search Form" layout is used, the search form starts out
expanded.

    >>> 'collapsedOnLoad' in anon_browser.contents
    False
    
Criterion fields that haven't been selected in "Form Fields" don't
appear on the search form.

    >>> form.getControl(
    ...     name='form_crit__SearchableText_ATSimpleStringCriterion'
    ...     '_formFields:list')
    Traceback (most recent call last):
    LookupError: name
    'form_crit__SearchableText_ATSimpleStringCriterion_formFields:list'

The label for the criterion corresponds to the form element for the
firs criterion field.

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

Since the search form has been submitted from the "Search Form"
layout, the results are rendered on the layout specified by the "Form
Results Layout" field and the search form starts out collapsed.

    >>> anon_browser.url.startswith(
    ...     'http://nohost/plone/Members/test_user_1_/foo-topic-title'
    ...     '/atct_topic_view')
    True
    >>> 'collapsedOnLoad' in anon_browser.contents
    True

The search form also reflects the search term submitted rather than
the default value submitted on the criteria tab.

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

Contents View
=============

Change the topic's display layout to the contents view.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('folder_contents_view').click()
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
    ...     name='form_crit__SearchableText_ATSimpleStringCriterion'
    ...     '_value').value = 'baz'
    >>> form.getControl(name='submit').click()
    >>> browser.getControl('Bar Document Title')
    Traceback (most recent call last):
    LookupError: label 'Bar Document Title'
    >>> browser.getControl('Baz Event Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/baz-event-title'
    selected=False>
