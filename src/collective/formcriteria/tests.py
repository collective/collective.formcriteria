import unittest
import doctest

from plone.testing import layered

from collective.formcriteria import testing

optionflags = (doctest.NORMALIZE_WHITESPACE |
               doctest.ELLIPSIS)


def test_suite():
    suite = layered(doctest.DocFileSuite(
        'README.rst',
        optionflags=optionflags),
                    layer=testing.CONTENT_FUNCTIONAL_TESTING)

    topic_suite = layered(doctest.DocFileSuite(
        'portlet/README.rst',
        optionflags=optionflags),
                    layer=testing.TOPIC_FUNCTIONAL_TESTING)

    criteria_suite = layered(doctest.DocFileSuite(
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
        optionflags=optionflags),
                    layer=testing.CRITERIA_FUNCTIONAL_TESTING)

    columns_suite = layered(doctest.DocFileSuite(
        'columns/README.rst',
        'foldercontents/README.rst',
        'csv/README.rst',
        optionflags=optionflags),
                    layer=testing.COLUMNS_FUNCTIONAL_TESTING)

    contents_suite = layered(doctest.DocFileSuite(
        'foldercontents/buttons.rst',
        'foldercontents/kss.rst',
        'foldercontents/sum.rst',
        optionflags=optionflags),
                    layer=testing.CONTENTS_FUNCTIONAL_TESTING)

    return unittest.TestSuite(
        [suite, topic_suite, criteria_suite, columns_suite,
        contents_suite])

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
