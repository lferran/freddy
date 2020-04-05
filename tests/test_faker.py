import unittest

import jsonschema
import jsonschema_faker


class TestBasicType(unittest.TestCase):
    def _makeOne(self, schema):
        return jsonschema_faker.generate(schema)


class TestBoolean(TestBasicType):
    def test_returns_bool(self):
        self.assertIsInstance(self._makeOne({"type": "boolean"}), bool)


class TestNull(TestBasicType):
    def test_returns_none(self):
        self.assertIsNone(self._makeOne({"type": "null"}))


class TestInteger(TestBasicType):
    def test_returns_integer(self):
        self.assertIsInstance(self._makeOne({"type": "integer"}), int)

    def test_min_max_returns_in_range(self):
        self.assertEqual(
            self._makeOne({"type": "integer", "minimum": 9, "maximum": 9}), 9
        )

    def test_exclusive_min_max_returns_in_range(self):
        self.assertEqual(
            self._makeOne(
                {
                    "type": "integer",
                    "minimum": 9,
                    "maximum": 10,
                    "exclusiveMinimum": True,
                }
            ),
            10,
        )
        self.assertEqual(
            self._makeOne(
                {
                    "type": "integer",
                    "minimum": 9,
                    "maximum": 10,
                    "exclusiveMaximum": True,
                }
            ),
            9,
        )


class TestString(TestBasicType):
    def test_returns_string(self):
        self.assertIsInstance(self._makeOne({"type": "string"}), str)

    def test_min_max_returns_in_length_range(self):
        self.assertEqual(
            len(self._makeOne({"type": "string", "minLength": 6, "maxLength": 6})), 6
        )
        self.assertIn(
            len(self._makeOne({"type": "string", "minLength": 0, "maxLength": 2})),
            range(0, 2),
        )


def test_dummy():
    tests = []
    tests.append({"type": "boolean"})
    tests.append({"type": "null"})
    tests.append({"type": "integer", "minimum": 2, "maximum": 7})
    tests.append({"type": "string", "minLength": 2, "maxLength": 10})
    tests.append({"type": "string", "enum": ["foo", "bar", "ba"]})
    tests.append(
        {
            "type": "array",
            "minItems": 1,
            "maxItems": 10,
            "items": {"type": "string", "enum": ["hello", "world"]},
        }
    )
    tests.append(
        {"type": "array", "minItems": 1, "maxItems": 10, "items": {"type": "boolean"}}
    )
    tests.append(
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 3, "maxLength": 10},
                "age": {"type": "integer", "minimum": 0, "maximum": 110},
            },
        }
    )
    tests.append(
        {
            "type": "object",
            "properties": {
                "name": {"type": "string", "minLength": 3, "maxLength": 10},
                "age": {"type": "integer", "minimum": 0, "maximum": 110},
                "passed": {"type": "boolean"},
                "criminal_records": {"type": "null"},
                "marks": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "subject": {"type": "string"},
                            "mark": {"type": "number", "maximum": 10, "minimum": 0},
                        },
                    },
                },
            },
        }
    )
    for schema in tests:
        sample = jsonschema_faker.generate(schema)
        jsonschema.validate(sample, schema)
