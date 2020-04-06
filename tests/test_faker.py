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
        jsonschema.validate(sample, schema)

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


person_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "surname": {"type": "string"},
        "age": {"type": "integer", "maximum": 100, "minimum": 0},
        "has_children": {"type": "boolean"},
    },
}
company_schema = {
    "definitions": {"person": person_schema},
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "ceo": {"$ref": "#/definitions/person"},
        "cfo": {"$ref": "#/definitions/person"},
    },
}


class TestGetDefinitionGenerator(unittest.TestCase):
    def _makeOne(self, schema):
        return jsonschema_faker.get_definition_generator(schema)

    def test_get_definition_generator_generates_correctly(self):
        person_generator = self._makeOne(person_schema)
        person = person_generator()
        self.assertIsInstance(person["name"], str)
        self.assertIsInstance(person["surname"], str)
        self.assertIsInstance(person["age"], int)
        self.assertIsInstance(person["has_children"], bool)

    def test_nested_definition_generates_correctly(self):
        person_generator = self._makeOne(company_schema)
        company = person_generator()
        self.assertIsInstance(company["name"], str)
        for boss in ("cfo", "ceo"):
            self.assertIsInstance(company[boss], dict)
            self.assertIsInstance(company[boss]["name"], str)
            self.assertIsInstance(company[boss]["surname"], str)
            self.assertIsInstance(company[boss]["age"], int)
            self.assertIsInstance(company[boss]["has_children"], bool)


class TestReferences(TestBasicType):
    def test_array_with_reference(self):
        schema = {
            "type": "array",
            "maxItems": 2,
            "items": {"$ref": "#/definitions/person"},
        }
        result = self._makeOne(team_schema)
