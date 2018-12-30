# log and load online users

import json


def log_online_users(client):
    with open("logs\\online_users.json", "w") as file:
        json.dump(client, file)


def read_online_users():
    with open("logs\\online_users.json", "r") as file:
        online_users = json.load(file)
        file.close()

        return online_users
