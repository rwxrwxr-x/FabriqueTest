from rest_framework.exceptions import NotFound


def not_found(model, action, value=None):
    try:
        question = getattr(model.objects, action)(
            **value if isinstance(value, dict) else value
        )
        return question
    except model.DoesNotExist:
        raise NotFound
