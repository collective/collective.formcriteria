from AccessControl import ClassSecurityInfo

from Products.Archetypes import atapi

class TopicContainer(base.NonRefCatalogContent):
    """A container for topic crtieria or columns"""

    security = ClassSecurityInfo()

    meta_type = portal_type = 'TopicContainer'
    archetype_name = 'Topic Container'

    schema = atapi.Schema((
        ))

atapi.registerType(TopicContainer, 'collective.formcriteria')
