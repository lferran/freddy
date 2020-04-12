import unittest

import freddy
import jsonschema
from freddy.freddy import get_definition_generator


class TestBasicType(unittest.TestCase):
    def _makeOne(self, schema):
        return freddy.jsonschema(schema)


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
        schema = {"type": "integer", "minimum": 9, "maximum": 9}
        sample = self._makeOne(schema)
        self.assertEqual(sample, 9)
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


class TestConst(TestBasicType):
    def test_returns_const(self):
        schema = {"type": "object", "properties": {"hello": {"const": "world"}}}
        self.assertEqual(self._makeOne(schema), {"hello": "world"})


class TestString(TestBasicType):
    def test_returns_string(self):
        self.assertIsInstance(self._makeOne({"type": "string"}), str)

    def test_min_max_returns_in_length_range(self):
        self.assertEqual(
            len(self._makeOne({"type": "string", "minLength": 6, "maxLength": 6})), 6
        )
        self.assertIn(
            len(self._makeOne({"type": "string", "minLength": 0, "maxLength": 2})),
            [0, 1, 2],
        )


class TestNumbers(TestBasicType):
    def test_returns_float(self):
        schema = {"type": "number"}
        self.assertIsInstance(self._makeOne(schema), float)

    def test_min_max_returns_in_length_range(self):
        schema = {"type": "number", "minimum": 10, "maximum": 20}
        result = self._makeOne(schema)
        assert 10 <= result <= 20

    def test_exclusive_min_max_returns_in_range(self):
        schema = {
            "type": "number",
            "minimum": 9,
            "maximum": 10,
            "exclusiveMinimum": True,
        }
        result = self._makeOne(schema)
        assert 9 < result <= 10


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
        return get_definition_generator(schema)

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
        team_schema = {
            "definitions": {"person": person_schema},
            "type": "array",
            "minItems": 5,
            "maxItems": 5,
            "items": {"$ref": "#/definitions/person"},
        }
        team = self._makeOne(team_schema)
        jsonschema.validate(team, team_schema)
        for person in team:
            self.assertIsInstance(person["name"], str)
            self.assertIsInstance(person["surname"], str)
            self.assertIsInstance(person["age"], int)
            self.assertIsInstance(person["has_children"], bool)
