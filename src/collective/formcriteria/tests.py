import unittest
import doctest

from Testing import ZopeTestCase
from Products.PloneTestCase import ptc

from collective.formcriteria import testing

optionflags = (doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS)


def test_suite():
    suite = ZopeTestCase.FunctionalDocFileSuite(
        'README.rst',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    suite.layer = testing.content_layer

    topic_suite = ZopeTestCase.FunctionalDocFileSuite(
        'portlet/README.rst',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    topic_suite.layer = testing.topic_layer

    criteria_suite = ZopeTestCase.FunctionalDocFileSuite(
        'criteria/list.rst',
        'criteria/selection.rst',
        'criteria/checkbox.rst',
        'criteria/pulldown.rst',
        'criteria/daterange.rst',
        'criteria/comma.rst',
        'criteria/boolean.rst',
        'criteria/date.rst',
        'criteria/path.rst',
        'criteria/relativepath.rst',
        'criteria/simpleint.rst',
        'criteria/sort.rst',
        'criteria/context.rst',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    criteria_suite.layer = testing.criteria_layer

    columns_suite = ZopeTestCase.FunctionalDocFileSuite(
        'columns/README.rst',
        'foldercontents/README.rst',
        'csv/README.rst',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    columns_suite.layer = testing.columns_layer

    contents_suite = ZopeTestCase.FunctionalDocFileSuite(
        'foldercontents/buttons.rst',
        'foldercontents/kss.rst',
        'foldercontents/sum.rst',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    contents_suite.layer = testing.contents_layer

    return unittest.TestSuite(
        [suite, topic_suite, criteria_suite, columns_suite,
        contents_suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
