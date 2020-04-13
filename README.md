# freddy

Provides randomized json data (samples) that complies with a given
json schema.

## Usage

```python
from pprint import pprint
import jsonschema
import freddy

family_schema = {
    "type": "array",
    "items": {
        "properties": {
            "member": {"$ref": "#/definitions/person"},
            "role": {"$ref": "#/definitions/role"},
        },
        "type": "object",
    },
    "maxItems": 5,
    "minItems": 1,
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
```

## Install

``` shell
pip install freddy
```

## Development

``` shell
# Clone the repo
git@github.com:lferran/freddy.git
cd freddy

make develop

# Run tests
make tests
```

## JSON Schema support

- [x] boolean type
- [x] null type
- [x] string type
- [x] number type
- [x] integer type
- [x] array type
- [x] object type
- [x] definitions/references
- [x] Boolean type
- [x] consts
- [x] number `multipleOf` keyword

- [ ] `required` keyword
- [ ] `additionalProperties`
- [ ] string `pattern` regex keyword
- [ ] string built-in formats
- [ ] be able to provide custom basic type factories
- [ ] multiple types: `{"type": ["string", "array"]}`
- [ ] look into `allOf`: generate multiple objects + merge

Does not support:

- ID referencing
- `allOf` and `not` keywords
- conditional keywords `if`, `then` and `else`
