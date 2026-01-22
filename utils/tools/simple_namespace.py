class SimpleNamespace:
    """
    Dynamically creates attributes from the passed key arguments.
    Supports adding new attributes after creation.
    There is a to_dict() method for conversion to a dictionary, which is convenient for JSON or logs.
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"NS({attrs})"

    def to_dict(self):
        return dict(self.__dict__)
