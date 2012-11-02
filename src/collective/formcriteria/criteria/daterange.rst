.. -*-doctest-*-

Date Range
==========

A criterion is provided for rendering two calendar widgets on the
search form to specify two dates for a date range query.

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

Before a criterion requiring JavaScript or CSS helpers has been added,
the collection view does not include any such helpers.

    >>> browser.open(foo_topic.absolute_url())
    >>> 'calendar_stripped.js' in browser.contents
    False
    >>> 'calendar_en.js' in browser.contents
    False
    >>> 'calendar-system.css' in browser.contents
    False

Add a date range criterion for the effective date

    >>> foo_topic.addCriterion(
    ...     'effective', 'FormDateRangeCriterion')
    <FormDateRangeCriterion at
    /plone/Members/test_user_1_/foo-topic-title/crit__effective_FormDateRangeCriterion>

Designate the criterion's field as a form field.

    >>> criterion = foo_topic.getCriterion(
    ...     'effective_FormDateRangeCriterion')
    >>> criterion.setFormFields(['start', 'end'])

The values set on the criterion are the default values on the search
form.

    >>> from collective.formcriteria.testing import CONTENT_FIXTURE
    >>> now = CONTENT_FIXTURE.now
    >>> effective_start = now-3
    >>> criterion.setStart(effective_start)
    >>> effective_end = now-1
    >>> criterion.setEnd(effective_end)

    >>> import transaction
    >>> transaction.commit()

When viewing the collection in a browser the date widgets will be
rendered for the index with the default values.

    >>> browser.open(foo_topic.absolute_url())

    >>> form = browser.getForm(name="formcriteria_search")
    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_start_year').getControl(str(effective_start.year())).selected
    True
    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_start_month').getControl(effective_start.Month()).selected
    True
    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_start_day').getControl(
    ...         value=str(effective_start.day()).zfill(2)).selected
    True

    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_end_year').getControl(str(effective_end.year())).selected
    True
    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_end_month').getControl(effective_end.Month()).selected
    True
    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_end_day').getControl(
    ...         value=str(effective_end.day()).zfill(2)).selected
    True

By default the hour and minute fields are hidden.

    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_start_hour').type
    'hidden'
    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_start_minute').type
    'hidden'

    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_end_hour').type
    'hidden'
    >>> form.getControl(
    ...     name='form_crit__effective_FormDateRangeCriterion'
    ...     '_end_minute').type
    'hidden'

The widget helper JavaScript and CSS will also be included on the page
when the search form is present and fields require it.

    >>> 'calendar_stripped.js' in browser.contents
    True
    >>> 'calendar-en.js' in browser.contents
    True
    >>> 'calendar-system.css' in browser.contents
    True

Though the fields are required for editing criteria, they are not
marked as required on the search form.

    >>> '(Required)' in browser.contents
    False

By default the criterion values determine the search results.

    >>> browser.getLink('Bar Document Title')
    <Link text='...Bar Document Title'
    url='http://nohost/plone/Members/test_user_1_/bar-document-title'>
    >>> browser.getLink('Baz Event Title')
    Traceback (most recent call last):
    LinkNotFoundError

Change the date range and search.  Simulate the effect of the
JavaScript by also changing the value of the hidden inputs.

    >>> from collective.formcriteria.testing import setATDateWidget
    >>> ignored = setATDateWidget(
    ...     form, effective_start + 2,
    ...     'crit__effective_FormDateRangeCriterion_start')
    >>> ignored = setATDateWidget(
    ...     form, effective_end + 2,
    ...     'crit__effective_FormDateRangeCriterion_end')
    >>> form.getControl(name='submit').click()

Now the default has been overriden by the submitted query.

    >>> browser.getLink('Bar Document Title')
    Traceback (most recent call last):
    LinkNotFoundError
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

The widget helper JavaScript and CSS will also be included when the
search form portlet is rendered outside the context of the collection.

    >>> browser.open(folder.absolute_url())
    >>> 'calendar_stripped.js' in browser.contents
    True
    >>> 'calendar-en.js' in browser.contents
    True
    >>> 'calendar-system.css' in browser.contents
    True

But the helpers are not included when the portlet is not rendered.

    >>> browser.open(portal.absolute_url())
    >>> 'calendar_stripped.js' in browser.contents
    False
    >>> 'calendar-en.js' in browser.contents
    False
    >>> 'calendar-system.css' in browser.contents
    False

Log in as a user that should see the editable border.

    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = testing.TEST_USER_NAME
    >>> browser.getControl(
    ...     'Password').value = testing.TEST_USER_PASSWORD
    >>> browser.getControl('Log in').click()

The editable border still appears when the portlet adds the helpers to
the HTML <head> element.

    >>> browser.open(folder.absolute_url())
    >>> 'calendar_stripped.js' in browser.contents
    True
    >>> 'calendar-en.js' in browser.contents
    True
    >>> 'calendar-system.css' in browser.contents
    True
    >>> browser.getLink('Edit')
    <Link text='Edit'
    url='http://nohost/plone/Members/test_user_1_/edit'>

Many form criteria
==================

When multiple date range criteria are used, the pagination links still work.

Add more date range form criteria.

    >>> daterange_fields = [
    ...     field for field, name, descr in foo_topic.listAvailableFields()
    ...     if 'FormDateRangeCriterion' in
    ...     foo_topic.allowedCriteriaForField(field)]
    >>> for field in daterange_fields:
    ...     criterion = foo_topic.addCriterion(
    ...         field, 'FormDateRangeCriterion')
    ...     criterion.setFormFields(['start', 'end'])

Set a very small batch size so that there are multiple pages of results.

    >>> foo_topic.update(itemCount=1)

Set values for all the daterange fields on all the content.

    >>> for event in folder.contentValues(dict(portal_type='Event')):
    ...     event.update(startDate=now, endDate=now, expirationDate=now+30)

    >>> import transaction
    >>> transaction.commit()

Enter form values for all the criteria and submit the search.

    >>> browser.open(foo_topic.absolute_url())
    >>> form = browser.getForm(name="formcriteria_search")
    >>> for crit in foo_topic.listSearchCriteria():
    ...     field = crit.Field()
    ...     ignored = setATDateWidget(
    ...         form, now - 365,
    ...         'crit__%s_FormDateRangeCriterion_start' % field)
    ...     ignored = setATDateWidget(
    ...         form, now + 365,
    ...         'crit__%s_FormDateRangeCriterion_end' % field)
    >>> form.getControl(name='submit').click()
    >>> print browser.contents
    <...
                    <h1...
                        Foo Topic Title...
                    </h1>...

The submitted search terms are selected in the widgets.

    >>> from pprint import pprint as pp
    >>> form = browser.getForm(name="formcriteria_search")
    >>> for crit in foo_topic.listSearchCriteria():
    ...     field = crit.Field()
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_start_year' % field
    ...         )
    ...     if not ctl.getControl(str((now-365).year())).selected:
    ...         ctl
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_start_month' % field
    ...         )
    ...     if not ctl.getControl((now-365).Month()).selected:
    ...         ctl
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_start_day' % field
    ...         )
    ...     if not ctl.getControl(value=str((now-365).day()).zfill(2)).selected:
    ...         ctl
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_start' % field
    ...         )
    ...     if ctl.value != str(now-365):
    ...         ctl
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_end_year' % field
    ...         )
    ...     if not ctl.getControl(str((now+365).year())).selected:
    ...         ctl
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_end_month' % field
    ...         )
    ...     if not ctl.getControl((now+365).Month()).selected:
    ...         ctl
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_end_day' % field
    ...         )
    ...     if not ctl.getControl(value=str((now+365).day()).zfill(2)).selected:
    ...         ctl
    ...     ctl = form.getControl(
    ...         name=
    ...         'form_crit__%s_FormDateRangeCriterion_end' % field
    ...         )
    ...     if ctl.value != str(now+365):
    ...         ctl

The search results include all items.

    >>> browser.getLink('Foo Event Title')
    <Link text='...Foo Event Title'
    url='http://nohost/plone/Members/test_user_1_/foo-event-title'>

Batching page links also work.

    >>> form = browser.getForm(name="navigation_form")
    >>> form.getControl(name="b_start", index=0).click()
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

    >>> form = browser.getForm(name="navigation_form")
    >>> form.getControl(name="b_start", index=0).click()
    >>> browser.getLink('Foo Event Title')
    <Link text='...Foo Event Title'
    url='http://nohost/plone/Members/test_user_1_/foo-event-title'>

    >>> form = browser.getForm(name="navigation_form")
    >>> form.getControl(name="b_start", index=1).click()
    >>> browser.getLink('Baz Event Title')
    <Link text='...Baz Event Title'
    url='http://nohost/plone/Members/test_user_1_/baz-event-title'>

    >>> form = browser.getForm(name="navigation_form")
    >>> form.getControl(name="b_start", index=1).click()
    >>> browser.getLink('Foo Event Title')
    <Link text='...Foo Event Title'
    url='http://nohost/plone/Members/test_user_1_/foo-event-title'>
