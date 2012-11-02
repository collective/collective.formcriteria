.. -*-doctest-*-

Path Criteria
=============

The FormPathCriterion is provided for rendering paths on the search
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

Add a path criterion for the subject/keywords.

    >>> foo_topic.addCriterion(
    ...     'path', 'FormPathCriterion')
    <FormPathCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__path_FormPathCriterion>

Designate the criterion's field as a form field.

    >>> crit = foo_topic.getCriterion('path_FormPathCriterion')
    >>> crit.setFormFields(['value', 'recurse'])

    >>> import transaction
    >>> transaction.commit()
    
When viewing the collection in a browser path fields will be
rendered for the field.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Search Sub-Folders')
    <ItemControl
    name='form_crit__path_FormPathCriterion_recurse:boolean'
    type='checkbox' optionValue='on' selected=False>

Also note that the primary 'value' field does not render the label for
the value field as it would be redundant.

    >>> '>Folders</label>' in browser.contents
    False
    >>> ('form_crit__path_FormPathCriterion_value_help'
    ...  in browser.contents)
    False
