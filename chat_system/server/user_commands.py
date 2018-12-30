from chat_system.server.logs import logging
from chat_system.server import STATICS


def commands(cmd):

    if cmd == "help":
        return help()

    elif cmd == "loadclients":
        try:
            return load_online_users()
        except Exception as e:
            print(e)

    elif cmd == "serverinfo":
        return server_information()

    else:
        return "[-] unknown command"


def help():
    help = "type\n" + \
           "    -c serverinfo to get server information\n" \
           "    -c loadclients to get the currently online clients"

    return help


def load_online_users():
    online = logging.read_online_users()

    users = ""
    for u in online:
        users += str(u) + " "

    return users


def server_information():
    info = "server information:\n" + " * version " + STATICS.VERSION + "\n" +\
           " * hosted by " + STATICS.HOST + "\n" + " * total clients registered " + str(STATICS.TOTAL_CLIENTS) + "\n"

    return info

