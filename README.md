# freddy

Provides randomized json data (samples) that complies with a given
json schema.

## Usage

```python
from freddy import Freddy

f = Freddy()

f.sample({"type": "string", "maximum": 10})
'leiod'

f.sample({"type": "string", "maximum": 10})
'nvf'

f.sample({"type": "array", "maxItems": 5, "items": {"type": "number", "maximum": 20}})
[14.264744308697502,
 2.7715877227063213,
 12.641121706942599,
 19.39264786907317,
 2.3200896382954506]

schema = {
    "definitions": {
        "person": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "children": {
                    "type": "array",
                    "maxItems": 2,
                    "items": {"$ref": "#/definitions/person"},
                    "default": []
                }
            }
        }
    },
    "type": "object",
    "properties": {
        "person": {"$ref": "#/definitions/person"}
    }
}

f.sample(schema)
{'person': {'name': 'uab',
  'children': [{'name': 'achyjtzwmv', 'children': []},
   {'name': 'hxazqvg',
    'children': [{'name': 'bkfvoraihx',
      'children': [{'name': 'nqshyrwjp',
        'children': [{'name': 'eyyfttxt', 'children': []},
         {'name': 'lhxmxj', 'children': []}]}]},
     {'name': 'elp', 'children': []}]}]}}


f.sample(schema)
{'person': {'name': 'nqguo',
  'children': [{'name': 'va', 'children': [{'name': 'i', 'children': []}]},
   {'name': 'vimkrcjkur', 'children': []}]}}
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

# Install pre-commit (optional)
pip install pre-commit
pre-commit install

# Run tests
pip install -e .[test]
pytest tests
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
- [ ] string regex
- [ ] string built-in formats
- [ ] be able to provide custom basic type factories

Does not support:

- `allOf` and `not` keywords
- conditional keywords `if`, `then` and `else`
