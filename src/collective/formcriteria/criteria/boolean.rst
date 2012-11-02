.. -*-doctest-*-

Boolean Criteria
================

The FormBooleanCriterion is provided for rendering booleans on the search
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

Add a boolean criterion for the subject/keywords.

    >>> foo_topic.addCriterion(
    ...     'is_folderish', 'FormBooleanCriterion')
    <FormBooleanCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__is_folderish_FormBooleanCriterion>

Designate the criterion's field as a form field.

    >>> crit = foo_topic.getCriterion('is_folderish_FormBooleanCriterion')
    >>> crit.setFormFields(['bool'])

    >>> import transaction
    >>> transaction.commit()
    
When viewing the collection in a browser boolean fields will be
rendered for the field.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Folder-like')
    <ItemControl
    name='form_crit__is_folderish_FormBooleanCriterion_bool:boolean'
    type='checkbox' optionValue='on' selected=False>

Also note that the primary 'bool' field does not render the label for
the value field as it would be redundant.

    >>> 'Value</label>' in browser.contents
    False
    >>> ('form_crit__is_folderish_FormBooleanCriterion_bool_help'
    ...  in browser.contents)
    False
