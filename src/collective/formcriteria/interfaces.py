from zope import interface


class IFormTopic(interface.Interface):
    """A topic providing the form criteria extensions."""


class IFormCriterion(interface.Interface):
    """A criterion that generates a search form field."""


class IFormCriteriaPortlet(interface.Interface):
    """The form criteria search form portlet."""


class IFormCriteriaLayer(interface.Interface):
    """The form criteria browser layer."""
