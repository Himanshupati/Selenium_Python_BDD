import json
import configparser

class PropertiesReader:
    def __init__(self, file_path):
        self.config = configparser.ConfigParser()
        self.config.read(file_path)

    def get_section(self, section):
        if not self.config.has_section(section):
            raise ValueError(f"Section '{section}' not found in the file")
        return self.Section(self.config, section)

    class Section:
        def __init__(self, config, section):
            self.config = config
            self.section = section

        def get_key(self, key):
            if not self.config.has_option(self.section, key):
                raise KeyError(f"Key '{key}' not found in '{self.section}'")
            return self.config.get(self.section, key)

        def __repr__(self):
            return f"<Section '{self.section}': {dict(self.config.items(self.section))}>"


# JSON Config Reader
class JsonConfigReader:
    def __init__(self, file_path):
        with open(file_path, 'r') as file:
            self.config = json.load(file)

    def get_section(self, section):
        if section not in self.config:
            raise ValueError(f"Section '{section}' not found in the JSON file")
        return self.Section(self.config, section)

    class Section:
        def __init__(self, config, section):
            self.config = config
            self.section = section

        def get_key(self, key):
            if key not in self.config[self.section]:
                raise KeyError(f"Key '{key}' not found in section '{self.section}'")
            return self.config[self.section][key]

        def __repr__(self):
            return f"<Section '{self.section}': {self.config[self.section]}>"


def load_config_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)
