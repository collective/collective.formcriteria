import unittest
from zope.testing import doctest

from Testing import ZopeTestCase
from Testing.ZopeTestCase.zopedoctest import functional
from Products.PloneTestCase import ptc

from collective.formcriteria import testing

optionflags = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)

orig_outstream_init = functional.DocResponseWrapper.__init__
def outstream_init(self, response, outstream, path, header_output):
    if not response.body:
        response.body = outstream.getvalue()
    orig_outstream_init(self, response, outstream, path,
                        header_output)

def test_suite():
    suite = ZopeTestCase.FunctionalDocFileSuite(
        'README.txt',
        'foldercontents/README.txt',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    suite.layer = testing.layer

    criteria_suite = ZopeTestCase.FunctionalDocFileSuite(
        'criteria/list.txt',
        'criteria/selection.txt',
        'criteria/checkbox.txt',
        'criteria/daterange.txt',
        'criteria/comma.txt',
        'criteria/boolean.txt',
        'criteria/date.txt',
        'criteria/path.txt',
        'criteria/relativepath.txt',
        'criteria/simpleint.txt',
        'criteria/sort.txt',
        'csv/README.txt',
        optionflags=optionflags,
        test_class=ptc.FunctionalTestCase)
    criteria_suite.layer = testing.criteria_layer

    return unittest.TestSuite([suite, criteria_suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
