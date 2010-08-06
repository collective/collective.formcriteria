import itertools
import operator

from zope.cachedescriptors import property


class GroupedListingView(object):
    """Lists items grouped by the sort used"""

    @property.Lazy
    def topicContents(self):
        return self.context.queryCatalog(batch=True)

    @property.Lazy
    def groups(self):
        query = self.context.buildQuery()
        assert 'sort_on' in query, (
            'The "Grouped Listing" layout requires a sort criterion')
        sort_on = query['sort_on']
        return (
            dict(key=key,
                 contents=list(contents))
            for key, contents in
            itertools.groupby(self.topicContents,
                              key=operator.attrgetter(sort_on)))
