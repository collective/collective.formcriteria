.. -*-doctest-*-

=======================
collective.formcriteria
=======================

This package extends the Products.ATContentTypes.criteria types to
create search forms.  Specifically, any criterion fields which are
selected in each criterion's "Form Fields" will be rendered on the
search form.  The values set on the criteria edit form become the
default values on the search form.  Search terms submitted through the
search form supplement any criteria not on the search form.  IOW,
criteria not appearing on the form become the base query built into
the search form.

.. contents:: Table of Contents

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

A CSV export action is also provided which provides a link to users
allowing them to download the collections results, subject to the
user's query in the CSV format.  This allows collections to be used,
for example, in conjunction with spreadsheet software for ad-hoc
reporting or limited export to other systems.

A folder contents table display layout is also included.  This layout
is not yet fully functional but provides the basis for some very rich
site admin functionality.

WARNING: Uninstall
==================

Uninstalling this product after having added any collections or adding
criteria to any collections, even ones added before install, is
untested and may leave your collections broken.

Form Criteria
=============

Start with some content for search results.

    >>> from Products.PloneTestCase import ptc
    >>> self.login()
    >>> self.folder['bar-document-title']
    <ATDocument at /plone/Members/test_user_1_/bar-document-title>
    >>> self.folder['baz-event-title']
    <ATEvent at /plone/Members/test_user_1_/baz-event-title>

Open a browser and log in as a normal user.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> browser.handleErrors = False
    >>> browser.open(portal.absolute_url())
    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = ptc.default_user
    >>> browser.getControl(
    ...     'Password').value = ptc.default_password
    >>> browser.getControl('Log in').click()

Add and publish a collection.

    >>> browser.open(folder.absolute_url())
    >>> browser.getLink('Collection').click()
    >>> browser.getControl('Title').value = 'Foo Topic Title'
    >>> browser.getControl('Save').click()
    >>> print browser.contents
    <...
    ...Changes saved...
    >>> foo_topic = folder['foo-topic-title']


    >>> browser.getLink('Submit').click()
    >>> print browser.contents
    <...
    ...Item state changed...

    >>> self.loginAsPortalOwner()
    >>> self.portal.portal_workflow.doActionFor(foo_topic, 'publish')
    >>> self.login()

Change the display layout of the collection to the "Search Form".

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
    'FormPulldownCriterion', 'FormSimpleStringCriterion',
    'FormListCriterion', 'FormCommaCriterion', 'FormSortCriterion',
    'FormContextCriterion']
    >>> foo_topic.allowedCriteriaForField(
    ...     'review_state', display_list=True)
    <DisplayList
    [('FormSelectionCriterion', 'Select values from list'),
     ('FormCheckboxCriterion', 'Check values'),
     ('FormPulldownCriterion', 'Select one value'),
     ('FormSimpleStringCriterion', 'Text'),
     ('FormListCriterion', 'List of values'),
     ('FormCommaCriterion', 'Enter comma separated values'),
     ('FormSortCriterion', 'Sort results'),
     ('FormContextCriterion',
      'Values will be taken from the context')] at ...>

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
    >>> 'formcriteria-portlet.css' in anon_browser.contents
    False

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
    >>> 'formcriteria-portlet.css' in anon_browser.contents
    True
    
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

Make sure none of the collective.formcriteria extensions interfere
with existing ATTopic instances.

    >>> browser.open(portal.events.aggregator.absolute_url())

All criteria can also be created using poral_types.constructContent.

    >>> self.loginAsPortalOwner()
    >>> foo_topic.deleteCriterion(
    ...     'crit__SearchableText_FormSimpleStringCriterion')
    >>> foo_topic.deleteCriterion(
    ...     'crit__review_state_FormSelectionCriterion')
    >>> seen = set()
    >>> topic_indexes = portal.portal_atct.topic_indexes
    >>> for field, index in sorted(topic_indexes.iteritems()):
    ...     for criterion in index.criteria:
    ...         if criterion in seen or criterion.startswith('AT'):
    ...             continue
    ...         portal.portal_types.constructContent(
    ...             criterion, foo_topic,
    ...             id='crit__%s_%s' % (field, criterion))
    ...         seen.add(criterion)
    'crit__Creator_FormSelectionCriterion'
    'crit__Creator_FormCheckboxCriterion'
    'crit__Creator_FormPulldownCriterion'
    'crit__Creator_FormSimpleStringCriterion'
    'crit__Creator_FormListCriterion'
    'crit__Creator_FormCommaCriterion'
    'crit__Creator_FormSortCriterion'
    'crit__Creator_FormContextCriterion'
    'crit__Date_FormDateCriterion'
    'crit__Date_FormDateRangeCriterion'
    'crit__Type_FormPortalTypeCriterion'
    'crit__Type_FormPortalTypeCheckboxCriterion'
    'crit__Type_FormPortalTypePulldownCriterion'
    'crit__UID_FormBooleanCriterion'
    'crit__UID_FormReferenceCheckboxCriterion'
    'crit__UID_FormReferenceCriterion'
    'crit__UID_FormReferencePulldownCriterion'
    'crit__UID_FormSimpleIntCriterion'
    'crit__path_FormPathCriterion'
    'crit__path_FormRelativePathCriterion'

Installing
==========

The 'default' profile is used when installing collective.formcriteria
through the Plone Add-ons control panel

    >>> portal.portal_quickinstaller.uninstallProducts(['collective.formcriteria'])
    >>> print portal.portal_quickinstaller.installProducts(['collective.formcriteria'])
        Installed Products
        ====================
        collective.formcriteria:ok:
    >>> portal.portal_quickinstaller.getInstallProfiles(
    ...     'collective.formcriteria')[0]
    u'collective.formcriteria:default'
