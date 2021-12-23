import json
import random

class Config():
    def __init__(self):
        self.hashtags = []
        self.comments = []

        #öffne json file und packe alle Daten in Variablen
        with open("settings.json") as jsonfile:
            data = json.load(jsonfile)

            for key, value in data.items():
                if key == "hashtags":
                    self.hashtags = value

                if key == "comments":
                    self.comments = value

                if key == "likestoday":
                    self.likestoday = int(value)

                if key == "commentstoday":
                    self.commentstoday = int(value)

    def random_hashtag(self):
        return random.choice(self.hashtags)

    def random_comment(self):
        return random.choice(self.comments)