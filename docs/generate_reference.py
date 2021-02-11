"""Generate README."""
import os
import re

from jinja2 import Environment, FileSystemLoader
import yaml
from yaml.loader import SafeLoader

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


def link_refs(string):
    """Hyperlink refs."""
    return re.sub(
        r"\"\$ref\": \"#/components/schemas/(\w+)\"",
        r"\"$ref\": \"(#/components/schemas/\g<1>)[\g<1>]\"",
        string,
    )


class SafeLineLoader(SafeLoader):
    def construct_mapping(self, node, deep=False):
        mapping = super().construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping['_start'] = node.start_mark.line
        mapping['_end'] = node.end_mark.line
        return mapping


def main():
    """Generate README."""
    yamlpath = os.path.join(
        THIS_DIR,
        "../TranslatorReasonerAPI.yaml",
    )

    j2_env = Environment(
        loader=FileSystemLoader(THIS_DIR),
        trim_blocks=False,
        keep_trailing_newline=True,
        extensions=[
            "jinja2.ext.do",
        ]
    )

    with open(yamlpath, 'r') as stream:
        data = yaml.load(stream, Loader=SafeLineLoader)
    components = data['components']
    schemas = components['schemas']
    markdown = j2_env.get_template('reference_template.md').render(
        schemas=schemas
    )

    with open('reference.md', 'w') as stream:
        stream.write(markdown)


if __name__ == "__main__":
    main()
