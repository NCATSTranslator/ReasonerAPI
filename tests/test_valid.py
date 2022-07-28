"""OpenAPI 3.0 validation."""
import json
import os
from pprint import pprint
import jsonschema
import requests
import yaml


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
    print(dir_path)
    with open(os.path.join(dir_path, '..', 'TranslatorReasonerAPI.yaml')) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)
    for filename in os.listdir(dir_path):
        f = os.path.join(dir_path, '../examples/Message', filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f) as f:
                example = yaml.load(f, Loader=yaml.SafeLoader)
                jsonschema.validate(example, spec)
