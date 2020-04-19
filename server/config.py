##
# Config Module
#
import os
import json

config_path = os.path.join(os.path.dirname(__file__), 'config.json')

# Object that allows dicts to be accessed via dot notation


class Config(dict):
    @staticmethod
    def process_value(v):
        if type(v) is dict:
            return Config(v)
        if type(v) is list:
            return list(map(Config.process_value, v))
        return v

    def __init__(self, *args, **kwargs):
        super(Config, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.items():
                    self[k] = Config.process_value(v)
                    # if type(v) is dict:
                    #     self[k] = Config(v)
                    # else:
                    #     self[k] = v

        if kwargs:
            for k, v in kwargs.items():
                self[k] = Config.process_value(v)
                # if type(v) is dict:
                #     self[k] = Config(v)
                # else:
                #     self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Config, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Config, self).__delitem__(key)
        del self.__dict__[key]


with open(config_path, 'r') as config_file:
    config_dict = json.load(config_file)
    config = Config(config_dict)
