.. -*-doctest-*-

Relative Path Criteria
======================

The FormRelativePathCriterion is provided for rendering a relative
path widget on the search form.

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
    ...     'path', 'FormRelativePathCriterion')
    <FormRelativePathCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__path_FormRelativePathCriterion>

Designate the criterion's field as a form field.

    >>> crit = foo_topic.getCriterion('path_FormRelativePathCriterion')
    >>> crit.setFormFields(['relativePath', 'recurse'])

    >>> import transaction
    >>> transaction.commit()
    
When viewing the collection in a browser path fields will be
rendered for the field.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Relative path')
    <Control
    name='form_crit__path_FormRelativePathCriterion_relativePath'
    type='text'>
