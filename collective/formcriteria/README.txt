.. -*-doctest-*-

=======================
collective.formcriteria
=======================

This package provides new criteria types based on the
ATContentTypes.criteria types that are used to create a form at the
top of the topic view.  Users can use the form to submit criteria to
supplement any search criteria in the topic.  Values entered on the
criteria tab for the topic become the default values on the form.

Also provided is an alternative display layout that uses the folder
contents table and can still display the search form viewlet.

Form Criteria
=============

Start with a collection and some content for search results.

    >>> from Products.PloneTestCase import ptc
    >>> self.login()
    >>> home = portal.portal_membership.getHomeFolder(ptc.default_user)
    >>> foo_topic = home['foo-topic-title']
    >>> foo_topic
    <ATTopic at /plone/Members/test_user_1_/foo-topic-title>
    >>> home['bar-document-title']
    <ATDocument at /plone/Members/test_user_1_/bar-document-title>
    >>> home['baz-document-title']
    <ATDocument at /plone/Members/test_user_1_/baz-document-title>

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

Before the topic has any form criteria, the serach form is not
present.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getForm(name="formcriteria_search")
    Traceback (most recent call last):
    LookupError

Add a simple string form criterion for searchable text on the criteria
tab.

    >>> browser.getLink('Criteria').click()
    >>> browser.getControl('Search Text').selected = True
    >>> browser.getControl(name="criterion_type", index=0).getControl(
    ...     'Form Text').selected = True
    >>> browser.getControl('Add criteria').click()
    >>> print browser.contents
    <...
    ...Search Text...
    ...A simple string form criterion...

Set a default search term.

    >>> browser.getControl(
    ...     name=
    ...     "crit__SearchableText_SimpleStringFormCriterion_value"
    ...     ).value = 'bar'
    >>> browser.getControl(name="form.button.Save").click()
    >>> print browser.contents
    <...
    ...Changes saved...

If no form value have been submitted, such as on a fresh load of the
topic view, the default term will be used in the query returning only
one of the documents.

    >>> len(foo_topic.queryCatalog())
    1

    >>> browser.getLink('View').click()
    >>> browser.getLink('Bar Document Title')
    <Link text='Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Document Title')
    Traceback (most recent call last):
    LinkNotFoundError

Now that a form criterion has been added, the topic view displays the
search form.

    >>> form = browser.getForm(name="formcriteria_search")

Enter a search term and submit the query.  The topic will now list the
other document.

    >>> form.getControl(name='SearchableText').value = 'baz'
    >>> form.getControl(name='submit').click()
    >>> browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> browser.getLink('Baz Document Title')
    <Link text='Baz Document Title'
    url='http://nohost/plone/Members/test_user_1_/baz-document-title'>

The search form also reflects the search term submitted rather than
the default value submitted on the criteria tab.

    >>> browser.getForm(name="formcriteria_search").getControl(
    ...     name='SearchableText').value
    'baz'

Contents View
=============

Change the topic's display layout to the contents view.

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
    >>> browser.getControl('Baz Document Title')
    Traceback (most recent call last):
    LookupError: label 'Baz Document Title'

The search form is also rendered if form criteria are present.

    >>> form = browser.getForm(name="formcriteria_search")

The contents view also reflects user submitted criteria.

    >>> form.getControl(name='SearchableText').value = 'baz'
    >>> form.getControl(name='submit').click()
    >>> browser.getControl('Bar Document Title')
    Traceback (most recent call last):
    LookupError: label 'Bar Document Title'
    >>> browser.getControl('Baz Document Title')
    <ItemControl name='paths:list' type='checkbox'
    optionValue='/plone/Members/test_user_1_/baz-document-title'
    selected=False>
