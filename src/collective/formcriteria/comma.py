from zope.cachedescriptors import property


class CommaWidgetView(object):

    @property.Lazy
    def macros(self):
        return self.index.macros
