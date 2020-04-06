# jsonschema-faker

Provides random fake data valid for a given json schema.

## Usage

```python
import jsonschema_faker

schema = {
    "definitions": {
        "person": {
            "type": "object",
            "properties": {
                "name": { "type": "string" },
                "children": {
                    "type": "array",
                    "maxItems": 2,
                    "items": { "$ref": "#/definitions/person" },
                    "default": []
                }
            }
        }
    },
    "type": "object",
    "properties": {
        "person": { "$ref": "#/definitions/person" }
    }
}

print(jsonschema_faker.generate(schema))
{'person': {'name': 'nqguo', 'children': [{'name': 'va', 'children': [{'name': 'i', 'children': []}]}, {'name': 'vimkrcjkur', 'children': []}]}}
```

## Install

``` shell
pip install jsonschema-faker
```


## Development

``` shell
git@github.com:lferran/jsonschema-faker.git
cd jsonschema-faker
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
- [] consts
- [] string regex
- [] string built-in formats
- [] number `multipleOf` keyword
- [] be able to provide custom basic type factories

### Does not support:

- `allOf` and `not` keywords
- conditional keywords `if`, `then` and `else`
