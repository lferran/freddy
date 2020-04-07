# freddy

Provides randomized json data (samples) that complies with a given
json schema.

## Usage

```python
from freddy import Freddy

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

f = Freddy()
print(f.sample(schema))
{'person': {'name': 'nqguo', 'children': [{'name': 'va', 'children': [{'name': 'i', 'children': []}]}, {'name': 'vimkrcjkur', 'children': []}]}}
```

## Development

``` shell
git@github.com:lferran/freddy.git
cd freddy
pip install -e .[test]
```

## Run tests

```shell
pytest tests/
```

## Json-schema support

- [x] boolean type
- [x] null type
- [x] string type
- [x] number type
- [x] integer type
- [x] array type
- [x] object type
- [x] definitions/references
- [x] Boolean type
- [ ] consts
- [ ] string regex
- [ ] string built-in formats
- [ ] number `multipleOf` keyword
- [ ] be able to provide custom basic type factories

### Does not support:

- `allOf` and `not` keywords
- conditional keywords `if`, `then` and `else`
