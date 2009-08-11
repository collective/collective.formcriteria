from plone.memoize import view

class SortView(object):

    @view.memoize
    def getSortInfo(self):
        form = self.request.form.copy()
        selected = None
        sorts = []
        criteria = self.context.listSortCriteria()
        for crit in criteria:
            sort = dict(
                id=crit.getId(),
                name=self.context.getFriendlyName(crit.Field()),
                selected=False)
            if sort['id'] in self.request:
                form.pop(sort['id'])
                selected = sort
                sort['selected'] = True
            sorts.append(sort)
        # If no sort is selected, use the first as the default
        if sorts and selected is None:
            selected = sorts[0]
            form.pop(selected['id'], None)
            sorts[0]['selected'] = True

        return dict(form=form, sorts=sorts, selected=selected)
