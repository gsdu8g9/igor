import yaml

class Config(object):
    config_path = "_config.yaml"

    defaults = {"summary_length": 0,
                "output_directory": "~blog",
                "blog_uri": ""}

    def __init__(self, project_path):
        self.project_path = project_path
        config_path = path.join(self.project_path, self.config_path)

        if path.exists(default_config_path):
            self.config = defauls.update(self.read(config_path))
        else:
            with open(config, 'w') as f:
                f.write(yaml.dump(self.defaults), default_flow_style=False)
                self.config = defaults

    def get(self, key):
        return self.config.get(key)

    def read(self, filename):
        with open(filename, 'r') as f:
            return yaml.load(f.read())
