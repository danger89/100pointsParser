import json


class Config:
    def __init__(self, param):
        self.path = "misc/config.json"
        self.param = param

    def get(self):
        with open(self.path) as input_file:
            return json.load(input_file)[self.param]

    def add(self, arg):
        with open(self.path) as input_file:
            data = json.load(input_file)

        if self.param == "courses_list":
            courses_list_new = list(set(data["courses_list"] + arg))
            data[self.param] = courses_list_new
        elif self.param == "last_homework_info":
            data[self.param] = arg

        with open(self.path, "w") as output_file:
            json.dump(data, output_file, ensure_ascii=False, indent=4)
