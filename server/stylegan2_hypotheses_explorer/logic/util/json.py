import json
from pathlib import Path
from typing import Dict, Union

from jsonschema import validate


def load(path: Path):
    with open(str(path.resolve()), "r") as file:
        return json.load(file)


def load_and_validate(resource: Path, schema: Union[Path, Dict]):
    resource = load(resource)
    if isinstance(schema, Path):
        schema = load(schema)
    validate(resource, schema)
    return resource
