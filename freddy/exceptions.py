from typing import Optional


class UnsupportedType(Exception):
    def __init__(self, _type):
        self._type = _type

    @property
    def type(self):
        return self._type


class UnsupportedSchema(Exception):
    def __init__(self, schema, reason: Optional[str] = None):
        self.schema = schema
        self.reason = reason


class InvalidSchema(Exception):
    def __init__(self, schema, reason: Optional[str] = None):
        self.schema = schema
        self.reason = reason
