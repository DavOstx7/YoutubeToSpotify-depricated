import json


class BaseJSONConfig:
    def __init__(self, file_path: str, *keys: str):
        with open(file_path, 'r') as file:
            config = json.load(file)
            for key in keys:
                config = config[key]
            self._config = config
