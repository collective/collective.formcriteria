.. -*-doctest-*-

List Criteria
=============

The FormListCriterion is provided for rendering lists on the search
form.

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
    ...     'Subject', 'FormListCriterion')
    <FormListCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__Subject_FormListCriterion>

Designate the criterion's field as a form field.

    >>> crit = foo_topic.getCriterion('Subject_FormListCriterion')
    >>> crit.setFormFields(['value'])
    
The values set on the criterion are the default values checked on the
search form.

    >>> crit.setValue(['bah'])

    >>> import transaction
    >>> transaction.commit()

When viewing the collection in a browser lists will be rendered
for the field with the default values selected.

    >>> browser.open(foo_topic.absolute_url())
    >>> ctrl = browser.getControl(
    ...     name='form_crit__Subject_FormListCriterion_value:lines')
    >>> ctrl
    <Control name='form_crit__Subject_FormListCriterion_value:lines'
    type='textarea'>
    >>> ctrl.value
    'bah'

By default the criterion values determine the search results.

    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError

Also note that criteria that use a 'value' field as the primary search
value do not render the label for the value field as it would be
redundant.

    >>> 'Values</label>' in browser.contents
    False
    >>> ('form_crit__Subject_FormListCriterion_value_help'
    ...  in browser.contents)
    False

Change the checked values and search

    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl(
    ...     name='form_crit__Subject_FormListCriterion_value:lines'
    ...     ).value = 'quux'
    >>> form.getControl(name='submit').click()

Now the default has been overriden by the submitted query.

    >>> browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

The operator may also be included on the form.

    >>> crit.setFormFields(['value', 'operator'])

    >>> import transaction
    >>> transaction.commit()

Use the default "or" search, and query on "bah" and "qux"

    >>> browser.open(foo_topic.absolute_url())
    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl('or').selected
    True
    >>> form.getControl(
    ...     name='form_crit__Subject_FormListCriterion_value:lines'
    ...     ).value = 'bah\nqux'
    >>> form.getControl(name='submit').click()

Both objects are returned when since both have "qux".

    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

Use the "and" and search operator with the same query.

    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl('and').selected = True
    >>> print form.getControl(
    ...     name='form_crit__Subject_FormListCriterion_value:lines'
    ...     ).value
    bah
    qux
    >>> form.getControl(name='submit').click()

Now only the object with both "bah" and "qux" is returned.

    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError

