import unittest
import doctest

from Testing import ZopeTestCase
from Products.PloneTestCase import ptc

from collective.formcriteria import testing

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

def test_suite():
    suite = ZopeTestCase.FunctionalDocFileSuite(
        'README.txt',
        'portlet/README.txt',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    suite.layer = testing.topic_layer

    criteria_suite = ZopeTestCase.FunctionalDocFileSuite(
        'criteria/list.txt',
        'criteria/selection.txt',
        'criteria/checkbox.txt',
        'criteria/pulldown.txt',
        'criteria/daterange.txt',
        'criteria/comma.txt',
        'criteria/boolean.txt',
        'criteria/date.txt',
        'criteria/path.txt',
        'criteria/relativepath.txt',
        'criteria/simpleint.txt',
        'criteria/sort.txt',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    criteria_suite.layer = testing.criteria_layer

    columns_suite = ZopeTestCase.FunctionalDocFileSuite(
        'columns/README.txt',
        'foldercontents/README.txt',
        'csv/README.txt',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    columns_suite.layer = testing.columns_layer

    contents_suite = ZopeTestCase.FunctionalDocFileSuite(
        'foldercontents/buttons.txt',
        'foldercontents/kss.txt',
        'foldercontents/sum.txt',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    contents_suite.layer = testing.contents_layer

    return unittest.TestSuite(
        [suite, criteria_suite, columns_suite, contents_suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
