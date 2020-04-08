from pprint import pprint

import jsonschema

import freddy

family_schema = {
    "type": "array",
    "minItems": 1,
    "maxItems": 5,
    "items": {
        "properties": {
            "member": {"$ref": "#/definitions/person"},
            "role": {"$ref": "#/definitions/role"},
        },
        "type": "object",
    },
    "definitions": {
        "person": {
            "properties": {
                "age": {"type": "integer"},
                "name": {"type": "string"},
                "pets": {
                    "items": {"$ref": "#/definitions/pet"},
                    "maxItems": 2,
                    "type": "array",
                },
            },
            "type": "object",
        },
        "pet": {
            "properties": {
                "kind": {"enum": ["dog", "cat"], "type": "string"},
                "name": {"type": "string"},
            },
            "type": "object",
        },
        "role": {
            "enum": [
                "father",
                "mather",
                "son",
                "daughter",
                "aunt",
                "grandma",
                "grandpa",
            ],
            "type": "string",
        },
    }
}

# Get 10 random samples
for i in range(10):
    sample_family = freddy.jsonschema(family_schema)

    # Validate against schema
    jsonschema.validate(sample_family, family_schema)

pprint(sample_family)
[
    {"member": {"age": 77, "name": "k", "pets": []}, "role": "grandma"},
    {"member": {"age": 64, "name": "naifvxf", "pets": []}, "role": "grandpa"},
    {
        "member": {
            "age": 23,
            "name": "itruydotrj",
            "pets": [{"kind": "cat", "name": "o"}, {"kind": "cat", "name": "uonmvfgd"}],
        },
        "role": "son",
    },
]
