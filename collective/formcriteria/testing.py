import DateTime
from Products.CMFPlone import utils as plone_utils

from Testing import ZopeTestCase
from Products.PloneTestCase import ptc

from Products.Five import zcml, fiveconfigure

from collective.testcaselayer import ptc as tcl_ptc

from collective import formcriteria

ptc.setupPloneSite()

class FormCriteriaLayer(tcl_ptc.BasePTCLayer):
    """Install collective.formcriteria"""

    def afterSetUp(self):
        fiveconfigure.debug_mode = True
        zcml.load_config('testing.zcml', package=formcriteria)
        fiveconfigure.debug_mode = False

        ZopeTestCase.installPackage('collective.formcriteria')

        self.addProfile('collective.formcriteria:default')
        self.addProfile('collective.formcriteria:testing')

        self.login()
        home = self.portal.portal_membership.getHomeFolder(
            ptc.default_user)
        plone_utils._createObjectByType(
            container=home, type_name='Topic',
            id='foo-topic-title', title='Foo Topic Title')

        self.now = DateTime.DateTime('Jan 15, 2009')
        home.invokeFactory(
            type_name='Document', effectiveDate=self.now-2,
            id='bar-document-title', title='Bar Document Title')
        home.invokeFactory(
            type_name='Event', effectiveDate=self.now,
            id='baz-event-title', title='Baz Event Title')

formcriteria_layer = FormCriteriaLayer([tcl_ptc.ptc_layer])
