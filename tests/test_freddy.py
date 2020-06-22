import unittest
from typing import List, Optional

import freddy
import jsonschema
import pydantic
import pytest


class TestBasicType(unittest.TestCase):
    def _makeOne(self, schema):
        # Get a sample
        sample = freddy.jsonschema(schema)
        # Validate it against schema
        jsonschema.validate(sample, schema)
        return sample


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
        self.assertEqual(self._makeOne(schema), 9)

    def test_exclusive_min_max_returns_in_range(self):
        self.assertEqual(
            self._makeOne({"type": "integer", "minimum": 9, "exclusiveMaximum": 10}), 9
        )
        self.assertEqual(
            self._makeOne({"type": "integer", "exclusiveMinimum": 9, "maximum": 10}), 10
        )


class TestConst(TestBasicType):
    def test_returns_const(self):
        schema = {
            "type": "object",
            "required": ["hello"],
            "properties": {"hello": {"const": "world"}},
        }
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
        schema = {"type": "number", "exclusiveMinimum": 9, "maximum": 10}
        result = self._makeOne(schema)
        assert 9 < result <= 10


class TestEnum(TestBasicType):
    def test_string_enum(self):
        enum = ["foo", "bar", "ba"]
        schema = {"type": "string", "enum": enum}
        self.assertIsInstance(self._makeOne(schema), str)
        self.assertIn(self._makeOne(schema), enum)

    def test_number_enum(self):
        enum = [1, 1.2, 3.3]
        schema = {"type": "number", "enum": enum}
        self.assertIn(type(self._makeOne(schema)), [float, int])
        self.assertIn(self._makeOne(schema), enum)


class TestObject(TestBasicType):
    def test_required(self):
        schema = {
            "type": "object",
            "required": ["bar"],
            "properties": {"foo": {"type": "string"}, "bar": {"type": "number"}},
        }
        sample = self._makeOne(schema)
        self.assertIsInstance(sample, dict)
        self.assertIn("bar", sample)


person_schema = {
    "type": "object",
    "required": ["name", "surname", "age", "has_children"],
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
    "required": ["name", "ceo", "cfo"],
    "properties": {
        "name": {"type": "string"},
        "ceo": {"$ref": "#/definitions/person"},
        "cfo": {"$ref": "#/definitions/person"},
    },
}


class TestGetDefinitionGenerator(TestBasicType):
    def test_get_definition_generator_generates_correctly(self):
        person = self._makeOne(person_schema)
        self.assertIsInstance(person["name"], str)
        self.assertIsInstance(person["surname"], str)
        self.assertIsInstance(person["age"], int)
        self.assertIsInstance(person["has_children"], bool)

    def test_nested_definition_generates_correctly(self):
        company = self._makeOne(company_schema)
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
        for person in team:
            self.assertIsInstance(person["name"], str)
            self.assertIsInstance(person["surname"], str)
            self.assertIsInstance(person["age"], int)
            self.assertIsInstance(person["has_children"], bool)


class Person(pydantic.BaseModel):
    name: str
    surname: str
    age: int
    has_children: bool
    pet_count: Optional[int] = 0
    nicknames: List[str]


class TestPydanticModel(unittest.TestCase):
    def _makeOne(self, model):
        return freddy.pydantic(model)

    def test_a_pydantic_model(self):
        person = self._makeOne(Person)
        self.assertIsInstance(person["name"], str)
        self.assertIsInstance(person["surname"], str)
        self.assertIsInstance(person["age"], int)
        self.assertIsInstance(person["has_children"], bool)
        self.assertIsInstance(person["nicknames"], list)
        for n in person["nicknames"]:
            self.assertIsInstance(n, str)
        if "pet_count" in person:
            self.assertIsInstance(person["pet_count"], int)


class Test_oneOf(TestBasicType):
    def test_schema_with_oneOf_at_top_level(self):
        schema = {
            "oneOf": [
                {"type": "array", "minItems": 20, "items": {"type": "number"}},
                {
                    "type": "object",
                    "required": ["foo"],
                    "properties": {"foo": {"type": "string", "minLength": 2}},
                },
            ]
        }
        sample = self._makeOne(schema)
        if isinstance(sample, dict):
            self.assertIsInstance(sample["foo"], str)
        elif isinstance(sample, list):
            for item in sample:
                self.assertIn(type(item), [int, float])
        else:
            raise Exception("something went wrong")


class Test_validate_schema(unittest.TestCase):
    def makeOne(self, *args, **kwargs):
        from freddy.freddy import _validate_schema

        _validate_schema(*args, **kwargs)

    def test_unsupported_json_schema_keys_raises_exception(self):
        from freddy.freddy import _unsupported_jsonschema_keys

        for jsonschema_key in _unsupported_jsonschema_keys:
            with pytest.raises(freddy.UnsupportedSchema) as ex:
                self.makeOne({jsonschema_key: "foobar"})
            self.assertEqual(ex.value.reason, f"{jsonschema_key} key is not supported")

    def test_multiple_types_not_supported(self):
        with pytest.raises(freddy.UnsupportedSchema) as ex:
            self.makeOne({"type": ["string", "number"]})
        self.assertEqual(ex.value.reason, "multiple types not supported yet")

    def test_definition_not_found(self):
        refname = "foobar"
        with pytest.raises(freddy.InvalidSchema) as ex:
            self.makeOne({"definitions": {}, "$ref": f"#/definitions/{refname}"})
        self.assertEqual(ex.value.reason, f"{refname} not present in definitions")

    def test_nor_ref_nor_type_nor_enum_nor_const(self):
        with pytest.raises(freddy.UnsupportedSchema) as ex:
            self.makeOne({})
        self.assertEqual(ex.value.reason, "type key is required")
