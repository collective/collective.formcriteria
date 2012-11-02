.. -*-doctest-*-

Selection Lists
===============

Three criterion are provided for rendering selection lists on the
search form: FormSelectionCriterion, FormPortalTypeCriterion,
FormReferenceCriterion.

We start with a topic.

    >>> from Products.CMFCore.utils import getToolByName
    >>> portal = layer['portal']
    >>> membership = getToolByName(portal, 'portal_membership')

    >>> from plone.app import testing
    >>> folder = membership.getHomeFolder(testing.TEST_USER_ID)
    >>> foo_topic = folder['foo-topic-title']

Open a browser as an anonymous user.

    >>> from plone.testing import z2
    >>> from plone.app import testing
    >>> browser = z2.Browser(layer['app'])
    >>> browser.handleErrors = False

Add a selection criterion for the subject/keywords.

    >>> foo_topic.addCriterion(
    ...     'Subject', 'FormSelectionCriterion')
    <FormSelectionCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__Subject_FormSelectionCriterion>

Designate the criterion's field as a form field.

    >>> crit = foo_topic.getCriterion(
    ...     'Subject_FormSelectionCriterion')
    >>> crit.setFormFields(['value'])

The values set on the criterion are the default values selected on the
search form.

    >>> crit.setValue(['bah'])

    >>> import transaction
    >>> transaction.commit()

When viewing the collection in a browser selections will be rendered
for the field with the default values selected.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('bah')
    <ItemControl
    name='form_crit__Subject_FormSelectionCriterion_value:list'
    type='select' optionValue='bah' selected=True>
    >>> browser.getControl('quux')
    <ItemControl
    name='form_crit__Subject_FormSelectionCriterion_value:list'
    type='select' optionValue='quux' selected=False>

By default the criterion values determine the search results.

    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError

Change the selected values and search

    >>> browser.getControl('bah').selected = False
    >>> browser.getControl('quux').selected = True
    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl(name='submit').click()

Now the default has been overriden by the submitted query.

    >>> browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>
