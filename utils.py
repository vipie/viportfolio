import json


class ConfigLoader:
    def __init__(self):
        with open('config.json') as f:
            self.config = json.load(f)

    @staticmethod
    def write_config_example():
        """
        Write config_example.json file for easy creation config.json
        :return:
        """
        data = {'provider': 'yahoo', 'msci_url':'test.url'}
        with open('config_example.json', 'w') as f:
            json.dump(data, f)


class LoadUniverse:
    """
    Load data from web
    """
    def __init__(self, config):
        pass