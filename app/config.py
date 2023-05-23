import os
import json
from typing import Any

class Config:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Config, cls).__new__(cls)
            config_path = os.environ.get("CONFIG_PATH", "/src/config.json")
            with open(config_path, "r") as config_file:
                cls.instance.config_json = json.load(config_file)
        return cls.instance

    def __getattr__(self, name: str) -> Any:
        return self.instance.config_json.get(name, None)
