import jsonschema


def test_dummy():
    tests = []
    tests.append(
        {"type": "boolean",}
    )
    tests.append({"type": "null"})
    tests.append(
        {"type": "integer", "minimum": 2, "maximum": 7,}
    )
    tests.append(
        {"type": "string", "minLength": 2, "maxLength": 10,}
    )
    tests.append(
        {"type": "string", "enum": ["foo", "bar", "ba"],}
    )
    tests.append(
        {
            "type": "array",
            "minItems": 1,
            "maxItems": 10,
            "items": {"type": "string", "enum": ["hello", "world"]},
        }
    )
    tests.append(
        {"type": "array", "minItems": 1, "maxItems": 10, "items": {"type": "boolean",}}
    )
    tests.append(
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 3, "maxLength": 10,},
                "age": {"type": "integer", "minimum": 0, "maximum": 110,},
            },
        }
    )
    tests.append(
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 3, "maxLength": 10,},
                "age": {"type": "integer", "minimum": 0, "maximum": 110,},
                "passed": {"type": "boolean"},
                "criminal_records": {"type": "null"},
                "marks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string"},
                            "mark": {"type": "number", "maximum": 10, "minimum": 0,},
                        },
                    },
                },
            },
        }
    )
    for schema in tests:
        sample = generate(schema)
        jsonschema.validate(sample, schema)
