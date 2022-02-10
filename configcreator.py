import json
import datetime


class Config(object):
    def __init__(self):
        with open("config.json") as json_file:
            data = json.load(json_file)
            self.test_guilds = data["test_guilds"]
            self.boottime = datetime.datetime.utcnow().timestamp()
            self.admins = data["admins"]

# >o)
# (_> HM
