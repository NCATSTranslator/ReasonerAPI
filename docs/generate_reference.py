"""Generate README."""

from pathlib import Path
import re
from typing import Any, Hashable, override

from jinja2 import Environment, FileSystemLoader
import yaml
from yaml.loader import SafeLoader

# So we can ensure we're going a directory up for the yaml
SCRIPT_DIR = Path(__file__).absolute().parent


def link_refs(string: str) -> str:
    """Hyperlink refs."""
    return re.sub(
        r"\"\$ref\": \"#/components/schemas/(\w+)\"",
        r"\"$ref\": \"(#/components/schemas/\g<1>)[\g<1>]\"",
        string,
    )


class SafeLineLoader(SafeLoader):
    @override
    def construct_mapping(
        self, node: yaml.MappingNode, deep: bool = False
    ) -> dict[Hashable, Any]:
        mapping = super().construct_mapping(node, deep=deep)
        # Add 1 so line numbering starts at 1
        mapping["_start"] = node.start_mark.line
        mapping["_end"] = node.end_mark.line
        return mapping


def main():
    """Generate README."""
    yamlpath = SCRIPT_DIR.parent.joinpath("TranslatorReasonerAPI.yaml")

    j2_env = Environment(
        loader=FileSystemLoader(SCRIPT_DIR),
        trim_blocks=False,
        keep_trailing_newline=True,
        extensions=[
            "jinja2.ext.do",
        ],
    )

    with yamlpath.open("r") as stream:
        data = yaml.load(stream, Loader=SafeLineLoader)
    components = data["components"]
    schemas = components["schemas"]

    sha = "master"

    markdown = j2_env.get_template("reference_template.md").render(
        schemas=schemas,
        sha=sha,
    )

    with Path("reference.md").open("w") as stream:
        _ = stream.write(markdown)


if __name__ == "__main__":
    main()
