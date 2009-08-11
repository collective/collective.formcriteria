.. -*-doctest-*-

========================
collective.catalogexport
========================

The data contained in tabular form in ZCatalogs is often exactly the
data site admins frequently want to export into some other format,
such as CSV.  This package provides views for exporting the catalog
data into various formats.

Currently, only exporting the whole catalog with all
metadata/brains/columns as CSV is supported.  I plan to add support
for submiting arbitrary index queries and for controlling the
metadata/brains/columns exported.

Start with a catalog with some indexes and metadata/brains/columns and
a few objects indexed.

    >>> self.folder.manage_addProduct['ZCatalog'].manage_addZCatalog(
    ...     'catalog', 'Catalog')
    >>> catalog = self.folder.catalog

    >>> catalog.addIndex('id', 'FieldIndex')
    >>> catalog.addIndex('title', 'FieldIndex')
    >>> catalog.indexes()
    ['id', 'title']

    >>> catalog.addColumn('meta_type')
    >>> catalog.addColumn('id')

    >>> self.folder.manage_addProduct['OFSP'].manage_addDTMLDocument(
    ...     'foo_doc', 'Foo Document')
    ''
    >>> catalog.catalog_object(self.folder.foo_doc)
    >>> self.folder.manage_addProduct['OFSP'].manage_addDTMLDocument(
    ...     'bar_doc', 'Bar Document')
    ''
    >>> catalog.catalog_object(self.folder.bar_doc)

    >>> [(brain.meta_type, brain.id) for brain in catalog()]
    [('DTML Document', 'foo_doc'), ('DTML Document', 'bar_doc')]

Open the export view in the browser specifying the export format as
CSV.

    >>> from Products.Five.testbrowser import Browser
    >>> from Testing import ZopeTestCase
    >>> self.setRoles(['Manager'])
    >>> browser = Browser()
    >>> browser.addHeader(
    ...     'Authorization', 'Basic %s:%s' %
    ...     (ZopeTestCase.user_name, ZopeTestCase.user_password))
    >>> browser.handleErrors = False
    >>> browser.open(catalog.absolute_url()+
    ...              '/export?Content-Type=text/csv')
    >>> browser.isHtml
    False
    >>> print browser.headers
    Status: 200 OK...
    Content-Disposition: attachment...
    Content-Type: text/csv...
    >>> print browser.contents

XXX the testbrowser doesn't handle use of response.write().  I've
verified that this works in a real browser::

    DTML Document,foo_doc
    DTML Document,bar_doc
