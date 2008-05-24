"""Add a form for user enterable search criteria to
collections/topic/smart folders."""

def initialize(context):
    from collective.formcriteria import criteria
    criteria # import to register
