from plone.memoize import view

class SortView(object):

    @view.memoize
    def getSortInfo(self):
        form = self.request.form.copy()
        selected = None
        ids = []
        sorts = {}
        criteria = self.context.listSortCriteria()
        for crit in criteria:
            field = crit.Field()
            sort = dict(
                id=crit.getId(),
                name=self.context.getFriendlyName(field),
                selected=False)
            if sort['id'] in self.request:
                form.pop(sort['id'])
                selected = sort
                sort['selected'] = True
            sorts[field] = sort
            ids.append(field)
        # If no sort is selected, use the first as the default
        if sorts and selected is None:
            selected = sorts[ids[0]]
            form.pop(selected['id'], None)
            selected['selected'] = True

        return dict(form=form, sorts=sorts, selected=selected,
                    ids=ids)
