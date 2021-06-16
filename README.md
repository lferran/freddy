# freddy

Provides randomized json data (samples) that complies with a given
schema.

Works both for json schema and pydantic models.

## Usage

### pydantic
```python
import datetime
from pprint import pprint
from typing import List, Optional
from pydantic import BaseModel, Field
import freddy


class User(BaseModel):
    id: int
    name = 'John Doe'
    signup_ts: Optional[datetime.datetime] = None
    friends: List[int] = []
    pattern_field: str = Field(..., regex=r"^[-_a-zA-Z0-9]+$")


sample = freddy.sample(User)
pprint(sample)
{'id': 357, 'friends': [308, 613, 549, 35, 869, 460, 630, 961], 'pattern_field': 'rI', 'name': 'yghyjdcsat'}
User.validate(sample)
User(id=565, signup_ts=datetime.datetime(1907, 6, 22, 18, 1), friends=[717, 235, 439, 589], pattern_field='rI', name='John Doe')
```

### jsonschema
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
    sample_family = freddy.sample(family_schema)

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

Conforms to JSON Schema Draft 7. The following features are supported:

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
- [x] `exclusiveMinimum` and `exclusiveMaximum` in integers and
      numbers.
- [x] number `multipleOf` keyword
- [x] string `pattern` regex keyword

- [ ] `required` keyword
- [ ] `additionalProperties`
- [ ] all string built-in formats
- [ ] be able to provide custom basic type factories
- [ ] multiple types: `{"type": ["string", "array"]}`
- [ ] look into `allOf`: generate multiple objects + merge

Does not support:

- ID referencing
- `allOf` and `not` keywords
- conditional keywords `if`, `then` and `else`
- `patternProperties` on objects
- property and schema `dependencies` on objects.
