class SortView(object):

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
                selected = crit
                sort['selected'] = True
            sorts.append(sort)
        if sorts and selected is None:
            form.pop(sorts[0]['id'], None)
            sorts[0]['selected'] = True

        return dict(form=form, sorts=sorts)
