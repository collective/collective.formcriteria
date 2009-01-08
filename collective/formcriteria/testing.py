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

formcriteria_layer = FormCriteriaLayer(
    [ptc.PloneTestCase.layer])
