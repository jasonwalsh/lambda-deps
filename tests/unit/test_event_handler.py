from functions.release import handler


def test_event_handler():
    event = {}
    context = None

    handler(event, context)
