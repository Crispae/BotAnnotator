# The Config class holds configuration data for multiple named entity recognition modules.
import json

# The Config class loads a JSON configuration file and provides methods to retrieve resources path and
# URL based on a given NER module.
class Config:
    def __init__(self, config_path):
        with open(config_path,"r") as file:
            self.config_data = json.load(file)

    def get_resources_path(self, ner_module):
        return self.config_data["path"][ner_module]

    def get_resources_url(self, ner_module):
        return self.config_data["url"][ner_module]
    


config_path = r"config.json"
config_info = Config(config_path=config_path) ### loading config file

