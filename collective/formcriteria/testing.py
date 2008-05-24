from Testing import ZopeTestCase
from Products.PloneTestCase import ptc as plone_ptc

from Products.Five import zcml, fiveconfigure

from collective.testcaselayer import ptc

from collective import formcriteria

plone_ptc.setupPloneSite()

class FormCriteriaLayer(ptc.BasePTCLayer):
    """Install collective.formcriteria"""

    def afterSetUp(self):
        fiveconfigure.debug_mode = True
        zcml.load_config('testing.zcml', package=formcriteria)
        fiveconfigure.debug_mode = False

        ZopeTestCase.installPackage('collective.formcriteria')

        self.addProfile('collective.formcriteria:default')
        self.addProfile('collective.formcriteria:testing')

formcriteria_layer = FormCriteriaLayer(
    [plone_ptc.PloneTestCase.layer])
