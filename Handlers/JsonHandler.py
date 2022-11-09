import json


class JsonHandler:
    def __init__(self, param):
        self.path = "config.json"
        self.param = param
        with open(self.path) as file:
            self.data = json.load(file)

    def read(self):
        return map(lambda x: x[1], self.data[self.param].items())

    def write(self, **kwargs):
        self.data[self.param] = kwargs

        with open(self.path, 'w') as output_file:
            json.dump(self.data, output_file, ensure_ascii=False, indent=4)
