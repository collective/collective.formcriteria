def setupColumnTemplate(context):
    if context.readDataFile(
        'collective.formcriteria.columns.txt') is None:
        return

    site = context.getSite()

    if 'templates' in site.contentIds():
        return
    topic = site[site.invokeFactory(
        type_name='Folder', id='templates',
        title='Content Templates')]

    if 'Topic' in site.templates.contentIds():
        return
    topic = site.templates[site.templates.invokeFactory(
        type_name='Topic', id='Topic')]

    searchable_query = topic.addCriterion(
        'SearchableText', 'FormSimpleStringCriterion')
    searchable_query.update(formFields=['value'])

    title_query = topic.addCriterion(
        'Title', 'FormSimpleStringCriterion')
    title_query.update(formFields=['value'])
    title_sort = topic.addCriterion(
        'sortable_title', 'FormSortCriterion')

    size_query = topic.addCriterion(
        'get_size', 'FormSimpleIntCriterion')
    size_query.update(formFields=['value', 'value2', 'direction'])
    size_sort = topic.addCriterion(
        'get_size', 'FormSortCriterion')

    modified_query = topic.addCriterion(
        'modified', 'FormDateCriterion')
    modified_query.update(
        formFields=['value', 'dateRange', 'operation'])
    modified_sort = topic.addCriterion(
        'modified', 'FormSortCriterion')

    state_query = topic.addCriterion(
        'review_state', 'FormSelectionCriterion')
    state_query.update(formFields=['value'])
    state_sort = topic.addCriterion(
        'review_state', 'FormSortCriterion')

    columns = topic[topic.invokeFactory(
        type_name='TopicColumns', id='columns', title='Columns')]
    columns.invokeFactory(
        type_name='TopicColumn', id='getPath-column', field='getPath',
        link=False, filter=searchable_query.getId())
    columns.invokeFactory(
        type_name='TopicColumn', id='Title-column', link=True,
         sort=title_sort.getId(), filter=title_query.getId())
    columns.invokeFactory(
        type_name='TopicColumn', id='get_size-column', link=False,
        sort=size_sort.getId(), filter=size_query.getId(),
        expression=(
            "python:modules['collective.formcriteria.columns.utils']"
            ".format_number(value)"))
    columns.invokeFactory(
        type_name='TopicColumn', id='ModificationDate-column',
        link=False,
        sort=modified_sort.getId(), filter=modified_query.getId())
    columns.invokeFactory(
        type_name='TopicColumn', id='review_state-column', link=False,
        sort=state_sort.getId(), filter=state_query.getId(),
        expression="python:"
        "portal.portal_workflow.getTitleForStateOnType(value, item.Type)")
