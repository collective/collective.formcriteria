.. -*-doctest-*-

Date Criteria
=============

The FormDateCriterion is provided for rendering relative date fields
on the search form.

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

Add a date criterion for the subject/keywords.

    >>> foo_topic.addCriterion(
    ...     'effectiveRange', 'FormDateCriterion')
    <FormDateCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__effectiveRange_FormDateCriterion>

Designate the criterion's field as a form field.

    >>> crit = foo_topic.getCriterion('effectiveRange_FormDateCriterion')
    >>> crit.setFormFields(['value', 'dateRange', 'operation'])

    >>> import transaction
    >>> transaction.commit()
    
When viewing the collection in a browser date fields will be
rendered for the field.

    >>> browser.open(foo_topic.absolute_url())
    >>> browser.getControl('Effective Range')
    <ListControl
    name='form_crit__effectiveRange_FormDateCriterion_value'
    type='select'>
