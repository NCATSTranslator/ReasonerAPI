"""OpenAPI 3.0 validation and examples validation."""
import json
from sys import stderr
import os
import pathlib
import jsonschema
import requests
import yaml
from jsonschema.exceptions import ValidationError
from reasoner_validator import TRAPISchemaValidator


def test_valid():
    """Test whether TranslatorReasonersAPI.yaml is valid OpenAPI 3.0."""
    response = requests.get('https://raw.githubusercontent.com/OAI/OpenAPI-Specification/master/schemas/v3.0/schema.json')
    openapi_schema = json.loads(response.text)

    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', 'TranslatorReasonerAPI.yaml')) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)

    jsonschema.validate(spec, openapi_schema)


def test_message_examples():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', 'TranslatorReasonerAPI.yaml')) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)
        print(spec)
    dir_path_json = os.path.join(dir_path, '../examples/Message')
    for filename in os.listdir(dir_path_json):
        full_path = os.path.join(dir_path_json, filename)
        file_extension = pathlib.Path(full_path).suffix
        if file_extension == '.json':
            with open(full_path) as f:
                print(full_path)
                example = json.load(f)
                trapi_version_locally = spec['info']['x-trapi']['version']
                validator = TRAPISchemaValidator(trapi_version=trapi_version_locally)
                print(validator.trapi_version)
                try:
                    validator.validate(
                        instance=example,
                        component="Message"
                    )
                except ValidationError:
                    print(validator.to_dict(), file=stderr)
                    raise ValueError('TRAPI example is not valid against the trapi_version specified!')


def metakg_examples():  # def test_metakg_examples():
    mtest_directory('../examples/MetaKnowledgeGraph', 'MetaKnowledgeGraph')
    mtest_directory('../examples/Message', 'Message')


def mtest_directory(json_path, object_to_validate):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, '..', 'TranslatorReasonerAPI.yaml')) as f:
        spec = yaml.load(f, Loader=yaml.SafeLoader)
    dir_path_json = os.path.join(dir_path, json_path)
    for filename in os.listdir(dir_path_json):
        full_path = os.path.join(dir_path_json, filename)
        file_extension = pathlib.Path(full_path).suffix
        if file_extension == '.json':
            with open(full_path) as f:
                example = json.load(f)
                trapi_version_locally = spec['info']['x-trapi']['version']
                validator = TRAPISchemaValidator(trapi_version=trapi_version_locally)
                try:
                    validator.validate(
                        instance=example,
                        component=object_to_validate
                    )
                except ValidationError:
                    print(validator.to_dict(), file=stderr)
                    raise ValueError('TRAPI example is not valid against the trapi_version specified!')