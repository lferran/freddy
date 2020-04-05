import string
import random
import json
from typing import Dict, Any, List, Union, Optional


"""
# todo
- add testing
- github actions
- complete support to basic types (as much as possible)
- support multiple types
- support const
- support definitions/refs
- regular expressions

# Does not support
- allOf
- not
- conditionals: if, then, else
"""


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


def _validate_schema(schema: Dict[str, Any]):
    """
    Raise error if schema is not one that we support
    """
    for unsupported in ("allOf", "not", "if", "then", "else"):
        if unsupported in schema:
            raise UnsupportedSchema(schema, reason=f"{unsupported} key is not supported")

    _type = schema.get("type")
    enum = schema.get("enum")
    if not _type and not enum:
        raise UnsupportedSchema(schema, reason=f"type key is required")


def sample(schema: Dict[str, Any]) -> str:
    return json.dumps(generate(schema))


def generate(schema: Dict[str, Any]) -> Any:
    _validate_schema(schema)

    for key in ("anyOf", "oneOf"):
        if key in schema:
            return generate_of(schema[key])

    if "enum" in schema:
        return generate_enum(schema["enum"])

    handlers = {
        "null": lambda s: None,
        "boolean": generate_boolean,
        "string": generate_string,
        "string": generate_string,
        "integer": generate_integer,
        "number": generate_number,
        "array": generate_array,
        "object": generate_object,
    }

    _type = schema["type"]
    try:
        handler = handlers[_type]
    except KeyError:
        raise UnsupportedType(_type)

    return handler(schema)


def generate_string(schema: Dict[str, Any]) -> str:
    minlength = schema.get("minLength", 0)
    maxlength = schema.get("maxLength", 10)
    length = random.randint(minlength, maxlength)
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_integer(schema : Dict[str, Any]) -> int:
    minimum = schema.get("minimum", 0)
    maximum = schema.get("maximum", 100)
    return random.randint(minimum, maximum)


def generate_number(schema : Dict[str, Any]) -> Union[int, float]:
    minimum = schema.get("minimum", 0)
    maximum = schema.get("maximum", 100)
    if random.randint(0, 1):
        return random.randint(minimum, maximum)
    return random.uniform(minimum, maximum)


def generate_enum(choices : List[Any]) -> Any:
    return random.choice(choices)


def generate_array(schema : Dict[str, Any]) -> List[Any]:
    maxitems = schema.get("maxItems", 10)
    minitems = schema.get("minItems", 0)
    items_schema = schema["items"]
    return [
        generate(items_schema)
        for i in range(random.randint(minitems, maxitems))
    ]


def generate_object(schema : Dict[str, Any]) -> Dict[str, Any]:
    return {
        key: generate(key_schema)
        for key, key_schema in schema.get("properties", {}).items()
    }

def generate_boolean(schema : Dict[str, Any]) -> bool:
    return random.choice([True, False])


def generate_of(schemas: List[Dict[str, Any]]) -> Any:
    return generate(random.choice(schemas))


if __name__ == "__main__":
    import jsonschema

    tests = []
    tests.append({
        "type": "boolean",
    })
    tests.append({
        "type": "null"
    })
    tests.append({
        "type": "integer",
        "minimum": 2,
        "maximum": 7,
    })
    tests.append({
        "type": "string",
        "minLength": 2,
        "maxLength": 10,
    })
    tests.append({
        "type": "string",
        "enum": ["foo", "bar", "ba"],
    })
    tests.append({
        "type": "array",
        "minItems": 1,
        "maxItems": 10,
        "items": {
            "type": "string",
            "enum": ["hello", "world"]
        }
    })
    tests.append({
        "type": "array",
        "minItems": 1,
        "maxItems": 10,
        "items": {
            "type": "boolean",
        }
    })
    tests.append({
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "minLength": 3,
                "maxLength": 10,
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "maximum": 110,
            },
        }
    })
    tests.append({
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "minLength": 3,
                "maxLength": 10,
            },
            "age": {
                "type": "integer",
                "minimum": 0,
                "maximum": 110,
            },
            "passed": {"type": "boolean"},
            "criminal_records": {
                "type": "null"
            },
            "marks": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "subject": {"type": "string"},
                        "mark": {
                            "type": "number",
                            "maximum": 10,
                            "minimum": 0,
                        }
                    }
                }
            }
        }
    })
    for schema in tests:
        sample = generate(schema)
        jsonschema.validate(sample, schema)
        print(f"{schema} --> {sample}")
