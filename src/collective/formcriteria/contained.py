class NonRefCatalogMixin(object):
    """Content that is neither referenceable nor in the catalog"""

    isReferenceable = None

    # reference register / unregister methods
    def _register(self, *args, **kwargs): pass
    def _unregister(self, *args, **kwargs): pass
    def _updateCatalog(self, *args, **kwargs): pass
    def _referenceApply(self, *args, **kwargs): pass
    def _uncatalogUID(self, *args, **kwargs): pass
    def _uncatalogRefs(self, *args, **kwargs): pass

    # catalog methods
    def indexObject(self, *args, **kwargs): pass
    def unindexObject(self, *args, **kwargs): pass
    def reindexObject(self, *args, **kwargs): pass
