import unittest
from zope.testing import doctest
from Testing import ZopeTestCase
from Products.Five import zcml

from collective import catalogexport

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

ZopeTestCase.installProduct('ZCatalog')

def setUp(test):
    zcml.load_config('tests.zcml', catalogexport)

def test_suite():
    return ZopeTestCase.FunctionalDocFileSuite(
        'README.txt',
        optionflags=optionflags,
        setUp=setUp,
        test_class=ZopeTestCase.FunctionalTestCase)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
