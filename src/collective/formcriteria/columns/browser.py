from zope.tal import taldefs

from Acquisition import aq_inner

from Products.Five.browser import pagetemplatefile

from plone.memoize import view


class ColumnsView(object):
    """Prepare and aggregate columns for use in browsr views"""

    def __init__(self, *args, **kw):
        super(ColumnsView, self).__init__(*args, **kw)
        (self.ordered, self.sorts, self.has_filters, self.has_sums
         ) = self.update()

    @view.memoize
    def update(self):
        engine = pagetemplatefile.getEngine()
        context = aq_inner(self.context)

        sort_info = context.restrictedTraverse(
            '@@sort_info').getSortInfo()
        crit_fields, criteria = context.restrictedTraverse(
            '@@criteria_form').criteriaFields()

        columns = getattr(context, 'columns', ())
        ordered = []
        sorts = {}
        has_filters = False
        has_sums = False
        for column_obj in columns and columns.contentValues():
            field = column_obj.Field()
            column = dict(
                field=field,
                name=column_obj.Title(),
                link=column_obj.getLink(),
                id_=column_obj.getId(),
                )

            sort = column_obj.getSort()
            if sort:
                sort_crit = context[sort]
                sort_field = sort_crit.Field()
                column['sort'] = sort_field
                sorts[sort_field] = sort_crit.getId()
                # Remove column sorts from the batch_macro sorts.
                # Only want to do this for views that use columns so
                # we modify the values from the sort_info view.
                # TODO This depends on memoize, maybe inappropriate
                sort_info['ids'].remove(sort_field)

            filter_ = column_obj.getFilter()
            if filter_:
                has_filters = True
                filter_field = context[filter_].Field()
                column['filter_'] = criteria[filter_field]
                # Remove column filters from the form criteria fields.
                # Only want to do this for views that use columns so
                # we modify the values from the criteria_form view.
                # TODO This depends on memoize, maybe inappropriate
                crit_fields.remove(filter_field)

            expr = column_obj.getExpression()
            if expr:
                key, expr = taldefs.parseSubstitution(expr)
                column['expr'] = engine.compile(expr)
                column['structure'] = (key == 'structure')

            column['has_sum'] = has_sum = column_obj.getSum()
            if has_sum:
                has_sums = True

            ordered.append(column)
        return ordered, sorts, has_filters, has_sums
