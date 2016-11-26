import os.path
import json


class JsonStorage:
    def __init__(self, path_to_dir, file_name):
        self.path_to_file = os.path.join(path_to_dir, "{0}.json".format(file_name))

    def load(self):
        if os.path.exists(self.path_to_file):
            with open(self.path_to_file, "r") as f:
                data = json.load(f)
        else:
            data = dict()
        return data

    def save(self, data):
        with open(self.path_to_file, "w") as f:
            json.dump(data, f, indent=1, sort_keys=True)
