"""Add a form for user enterable search criteria to
collections/topic/smart folders."""

from Products.CMFCore import utils 

from Products.Archetypes import atapi
from Products.ATContentTypes import permission

def initialize(context):
    from collective.formcriteria import criteria
    criteria # import to register

    from collective.formcriteria import topic
    topic # import to register

    listOfTypes = atapi.listTypes('collective.formcriteria')

    content_types, constructors, ftis = atapi.process_types(
        listOfTypes,
        'collective.formcriteria')

    allTypes = zip(content_types, constructors)
    for atype, constructor in allTypes:
        kind = "%s: %s" % (
            'collective.formcriteria', atype.archetype_name)
        utils.ContentInit(
            kind, content_types=(atype,),
            permission=permission.AddTopics,
            extra_constructors=(constructor,)).initialize(context)
