"""
Application specific errors.
"""


class CardError(Exception):
    """
    Base class for get_card_record errors.
    """


class CardNotFound(CardError, KeyError):
    """
    Error raised if a card number is not stored on the controller.
    """


class CardDeleted(CardError):
    """
    Error raised if a card number has been deleted from the controller.
    """


class EventBufferError(Exception):
    """
    Base class for get_event_record errors.
    """


class EventNotFound(EventBufferError):
    """
    Error raised if the event index is greater than the last event stored on the controller.
    """


class EventOverwritten(EventBufferError):
    """
    Error raised if the event index is less than the first event stored on the controller.
    """


class InvalidResponse(Exception):
    """
    Base class for errors raised because the response controller or card is incorrect
    """
