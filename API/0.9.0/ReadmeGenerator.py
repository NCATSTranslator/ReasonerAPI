# Class for autogenerating content for the README.md file based on the YAML file
import os
import sys
import re

class ReadmeGenerator:
  def __init__(self):
    self.read_api_file()

  #### Define attribute questions
  @property
  def questions(self) -> str:
    return self._questions

  @questions.setter
  def questions(self, questions: list):
    self._questions = questions

  def read_api_file(self):
    with open(os.path.join(os.path.dirname(__file__), 'TranslatorReasonersAPI_0.9.0.yaml'), 'r') as fid:
      state = "beginning"
      yaml_class = ""
      attribute_name = "??"
      type = "??"
      description = "??"
      example = ""
      questions = []
      for line in fid.readlines():
        if line[0] == "#":
          continue
        if state == "beginning":
          if re.match("definitions:",line):
            state = "definitions"
          continue

        match = re.match("  (\S+):",line)
        if match:
          yaml_class = match.group(1)
          print("- **"+attribute_name+"** - "+type+" - "+description+" (e.g.: "+example+")")
          attribute_name = "??"
          type = "??"
          description = "??"
          example = ""
          print()
          print("## "+yaml_class)

        match = re.match("      (\S+):",line)
        if match:
          if attribute_name != "??":
            print("- **"+attribute_name+"** - "+type+" - "+description+" (e.g.: "+example+")")
          attribute_name = "??"
          type = "??"
          description = "??"
          example = ""
          attribute_name = match.group(1)

        match = re.match("        type:(.+)",line)
        if match:
          type = match.group(1)
          type = re.sub("^\s*\"", "", type)
          type = re.sub("\"\s*", "", type)

        match = re.match("        description:(.+)",line)
        if match:
          description = match.group(1)
          description = re.sub("^\s*\"", "", description)
          description = re.sub("\"\s*", "", description)

        match = re.match("        example:(.+)",line)
        if match:
          example = match.group(1)
          

    print("- **"+attribute_name+"** - "+type+" - "+description+" (e.g.: "+example+")")

def main():
  readme = ReadmeGenerator()

if __name__ == "__main__":
  main()
