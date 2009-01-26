.. -*-doctest-*-

=======================
collective.formcriteria
=======================

This package provides extends the Products.ATContentTypes.criteria
types to create a search form at the top of the topic view.  If any of
the criterion fields are selected in the criterion's "Form Fields"
field, then those fields will be rendered on the search form.  Users
can use the form to submit criteria to supplement any search criteria
in the topic.  Values entered on the criteria tab for the topic become
the default values on the form.

Also provided is an alternative display layout that uses the folder
contents table and can still display the search form viewlet.

Form Criteria
=============

Start with a collection and some content for search results.

    >>> from Products.PloneTestCase import ptc
    >>> self.login()
    >>> foo_topic = self.folder['foo-topic-title']
    >>> foo_topic
    <ATTopic at /plone/Members/test_user_1_/foo-topic-title>
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

Add a criterion for the workflow state that won't appear on the form.
Then set the query term to return only published content.

    >>> browser.open(foo_topic.absolute_url()+'/criterion_edit_form')
    >>> form = browser.getForm(name='criteria_select')
    >>> form.getControl('State').selected = True
    >>> form.getControl(
    ...     'Select values from list', index=0).selected = True
    >>> form.getControl('Add criteria').click()
    >>> print browser.contents
    <...
    ...State...
    ...Select values from list...

    >>> browser.getControl('published').selected = True
    >>> browser.getControl('Save', index=0).click()
    >>> print browser.contents
    <...
    ...Changes saved...

Before the topic has any form criteria, the serach form is not
present.

    >>> browser.getLink('View').click()
    >>> browser.getForm(name="formcriteria_search")
    Traceback (most recent call last):
    LookupError

Add a simple string criterion for searchable text on the criteria tab.

    >>> browser.getLink('Criteria').click()
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
    ...     name='crit__SearchableText_SimpleStringFormCriterion'
    ...     '_formFields:list').getControl('Value').selected = True

Set a default search term.

    >>> browser.getControl(
    ...     name="crit__SearchableText_SimpleStringFormCriterion"
    ...     "_value").value = 'bar'
    >>> browser.getControl(name="form.button.Save").click()
    >>> print browser.contents
    <...
    ...Changes saved...

Open another browser as an anymous user.

    >>> anon_browser = Browser()
    >>> anon_browser.handleErrors = False
    >>> anon_browser.open(foo_topic.absolute_url())

If no form value have been submitted, such as on a fresh load of the
topic view, the default term will be used in the query returning only
one of the content objects.

    >>> len(foo_topic.queryCatalog())
    1

    >>> anon_browser.getLink('Bar Document Title')
    <Link text='Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> anon_browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError

Now that a form criterion has been added, the topic view displays the
search form.

    >>> form = anon_browser.getForm(name="formcriteria_search")

Since the search form has not been submitted, the search form starts
out expanded.

    >>> 'collapsedOnLoad' in anon_browser.contents
    False
    
Criterion fields that haven't been selected in "Form Fields" don't
appear on the search form.

    >>> form.getControl(
    ...     name='form_crit__SearchableText_SimpleStringFormCriterion'
    ...     '_formFields:list')
    Traceback (most recent call last):
    LookupError: name
    'form_crit__SearchableText_SimpleStringFormCriterion_formFields:list'

Enter a search term and submit the query.  The topic will now list the
other content object.

    >>> form.getControl(
    ...     name='form_crit__SearchableText_SimpleStringFormCriterion'
    ...     '_value').value = 'baz'
    >>> form.getControl(name='submit').click()
    >>> anon_browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> anon_browser.getLink('Baz Event Title')
    <Link text='Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

Since the search form has been submitted, the search form starts
out collapsed.

    >>> 'collapsedOnLoad' in anon_browser.contents
    True

The search form also reflects the search term submitted rather than
the default value submitted on the criteria tab.

    >>> anon_browser.getForm(name="formcriteria_search").getControl(
    ...     name='form_crit__SearchableText_SimpleStringFormCriterion'
    ...     '_value').value
    'baz'

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
    ...     name='form_crit__SearchableText_SimpleStringFormCriterion'
    ...     '_value').value = 'baz'
    >>> form.getControl(name='submit').click()
    >>> browser.getControl('Bar Document Title')
    Traceback (most recent call last):
    LookupError: label 'Bar Document Title'
    >>> browser.getControl('Baz Event Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/baz-event-title'
    selected=False>
