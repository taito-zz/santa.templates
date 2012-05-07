from zope.i18nmessageid import MessageFactory


_ = MessageFactory("santa.templates")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
