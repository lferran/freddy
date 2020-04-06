# jsonschema-faker

Provides random fake data valid for a given json schema.

## Usage

``` python
import jsonschema_faker

schema = {
    "definitions": {
        "person": {
            "type": "object",
            "properties": {
                "name": { "type": "string" },
                "children": {
                    "type": "array",
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

jsonschema_faker.generate(schema)
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
