"""OpenAPI 3.0 validation and examples validation."""
import json
import os
import pathlib
import jsonschema
import requests
import yaml
from jsonschema.exceptions import ValidationError
from reasoner_validator import validate


def test_valid():
    """Test whether TranslatorReasonersAPI.yaml is valid OpenAPI 3.0."""
    response = requests.get('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/schemas/v3.0/schema.json')
    openapi_schema = json.loads(response.text)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', 'TranslatorReasonerAPI.yaml')) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)

    jsonschema.validate(spec, openapi_schema)


def test_examples():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', 'TranslatorReasonerAPI.yaml')) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)
    dir_path_json = os.path.join(dir_path, '../examples/Message')
    for filename in os.listdir(dir_path_json):
        full_path = os.path.join(dir_path_json, filename)
        file_extension = pathlib.Path(full_path).suffix
        if file_extension == '.json':
            with open(full_path) as f:
                print(full_path)
                example = json.load(f)
                trapi_version_locally = spec['info']['x-trapi']['version']

                try:
                    validate(
                        instance=example,
                        component="Message",
                        trapi_version=trapi_version_locally
                    )
                except ValidationError:
                    raise ValueError('TRAPI example is not valid against the trapi_version specified!')

