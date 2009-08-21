.. -*-doctest-*-

Contents View
=============

Add a simple string criterion for the SearchableText index on the
criteria tab.  Set a default search term.

    >>> foo_topic = self.folder['foo-topic-title']
    >>> crit = foo_topic.addCriterion(
    ...     'SearchableText', 'FormSimpleStringCriterion')
    >>> crit.setValue('bar')
    >>> crit.setFormFields(['value'])

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

Search Form Portlet
-------------------

Add the portlet.

    >>> from zope import component
    >>> from plone.i18n.normalizer import (
    ...     interfaces as normalizer_ifaces)
    >>> from collective.formcriteria import portlet
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

The search form is also rendered if form criteria are present.

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
