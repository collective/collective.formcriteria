.. -*-doctest-*-

Integer Criteria
================

The FormSimpleIntCriterion is provided for rendering integer search
widgets on the search form.

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

Add a list criterion for the subject/keywords.

    >>> foo_topic.addCriterion(
    ...     'foo_int', 'FormSimpleIntCriterion')
    <FormSimpleIntCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__foo_int_FormSimpleIntCriterion>

Designate the criterion's field as a form field.

    >>> crit = foo_topic.getCriterion(
    ...     'foo_int_FormSimpleIntCriterion')
    >>> crit.setFormFields(['value', 'value2', 'direction'])

    >>> import transaction
    >>> transaction.commit()

When viewing the collection in a browser the fields will be rendered.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Foo Integer')
    <Control
    name='form_crit__foo_int_FormSimpleIntCriterion_value'
    type='text'>

Also note that criteria that use a 'value' field as the primary search
value do not render the label for the value field as it would be
redundant.

    >>> '>Value</label>' in browser.contents
    False
    >>> ('form_crit__foo_int_FormSimpleIntCriterion_value_help'
    ...  in browser.contents)
    False

Ensure that the criterion is registered for the right package.

    >>> from Products.Archetypes import ATToolModule
    >>> ATToolModule.getType(
    ...     'FormSimpleIntCriterion',
    ...     'collective.formcriteria')['package']
    'collective.formcriteria'

Without any value set, all objects appear.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

Submit a search query.

    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl('Foo Integer').value = '0'
    >>> form.getControl('Second Value').value = '1'
    >>> form.getControl('Between').selected = True
    >>> form.getControl(name='submit').click()
    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError
