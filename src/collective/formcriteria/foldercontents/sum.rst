.. -*-doctest-*-

Column Sums
-----------

The "Sum Colums" collection field specifies which of the columns
specified in the "Table Colums" will include a sum total of the values
for that column in a table head and foot row.

Note that since column fields have no types specified, it is up to the
user to select only columns that can be summed.

Set the batch size to force batching.

    >>> from plone.testing import z2
    >>> from plone.app import testing
    >>> portal = layer['portal']
    >>> z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)

    >>> from Products.CMFCore.utils import getToolByName
    >>> membership = getToolByName(portal, 'portal_membership')
    >>> folder = membership.getHomeFolder(testing.TEST_USER_ID)

    >>> foo_topic = folder['foo-topic-title']
    >>> foo_topic.update(itemCount=2)

Remove the sort criteria.

    >>> columns = foo_topic.columns
    >>> columns['getPath-column'].update(filter='')
    >>> columns['Title-column'].update(sort='', filter='')
    >>> columns['get_size-column'].update(sort='', filter='')
    >>> columns['ModificationDate-column'].update(sort='', filter='')
    >>> columns['review_state-column'].update(sort='', filter='')
    >>> foo_topic.manage_delObjects(
    ...     ['crit__sortable_title_FormSortCriterion',
    ...      'crit__get_size_FormSortCriterion',
    ...      'crit__modified_FormSortCriterion',
    ...      'crit__review_state_FormSortCriterion'])
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

Open a browser and log in.

    >>> browser = z2.Browser(layer['app'])
    >>> browser.handleErrors = False
    >>> browser.open(portal.absolute_url())
    >>> browser.getLink('Log in').click()
    >>> browser.getControl('Login Name').value = testing.TEST_USER_NAME
    >>> browser.getControl(
    ...     'Password').value = testing.TEST_USER_PASSWORD
    >>> browser.getControl('Log in').click()

If no column is set to calculate sums, no total rows are included in
either the table head or foot.

    >>> browser.open(foo_topic.absolute_url())
    >>> print browser.contents
    <...
          <thead...
            <tr>
              <th class="nosort"...>&#160;</th>
              <th class="nosort noSortColumn"
                  id="foldercontents-Title-column">
                    &#160;
                    Title
                    &#160;
                  </th>
              <th class="nosort noSortColumn"
                  id="foldercontents-get_size-column">
                    &#160;
                    Size
                    &#160;
                  </th>
              <th class="nosort noSortColumn"
                  id="foldercontents-ModificationDate-column">
                    &#160;
                    Modification Date
                    &#160;
                  </th>
              <th class="nosort noSortColumn"
                  id="foldercontents-review_state-column">
                    &#160;
                    State
                    &#160;
                  </th>
            </tr>
          </thead...
          <tfoot>
            <tr>
              <th colspan="5" class="nosort">
                <a id="foldercontents-show-all"...
          </tfoot...

Select the size column as a sum column.

    >>> z2.login(portal.getPhysicalRoot().acl_users, testing.SITE_OWNER_NAME)
    >>> foo_topic.columns['get_size-column'].update(sum=True)
    >>> testing.logout()

    >>> import transaction
    >>> transaction.commit()

A total sum is now included for the size column in the table head and
foot.

    >>> browser.open(foo_topic.absolute_url())
    >>> print browser.contents
    <...
          <thead...
            <tr>
                <th class="nosort"...>&#160;</th>
                  <th class="nosort noSortColumn"
                      id="foldercontents-Title-column">
                    &#160;
                    Title
                    &#160;
                  </th>
                  <th class="nosort noSortColumn"
                      id="foldercontents-get_size-column">
                    &#160;
                    Size
                    &#160;
                  </th>
                  <th class="nosort noSortColumn"
                      id="foldercontents-ModificationDate-column">
                    &#160;
                    Modification Date
                    &#160;
                  </th>
                  <th class="nosort noSortColumn"
                      id="foldercontents-review_state-column">
                    &#160;
                    State
                    &#160;
                  </th>
            </tr>
            <tr>
                <th class="nosort"...>&#160;Total&#160;</th>
                <th class="nosort columnSum">
                  &#160;
                </th>
                <th class="nosort columnSum">
                  &#160;
                    2.9 kB
                    &#160;
                </th>
                <th class="nosort columnSum">
                  &#160;
                </th>
                <th class="nosort columnSum">
                  &#160;
                </th>
            </tr>...
          <tfoot>
            <tr>
                <th class="nosort"...>&#160;Total&#160;</th>
                <th class="nosort columnSum">
                  &#160;
                </th>
                <th class="nosort columnSum">
                  &#160;
                    2.9 kB
                    &#160;
                </th>
                <th class="nosort columnSum">
                  &#160;
                </th>
                <th class="nosort columnSum">
                  &#160;
                </th>
            </tr>...
