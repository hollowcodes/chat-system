import socket
import time

from chat_system.server.logs import logging
from chat_system.server import encryption_processing, user_commands, STATICS
from chat_system.server.sql_database.sql_handler import database


class server:

    # init
    def __init__(self):

        self.SERVER_IP = STATICS.SERVER_IP
        self.PORT = STATICS.PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.clients = []
        self.clients_id = []

    # log clients
    def log_client(self, client, data):

        if client not in self.clients:
            id = encryption_processing.decrypt(data).split(" ")[0]

            self.clients.append(client)
            self.clients_id.append(id)

            logging.log_online_users(self.clients_id)

            STATICS.TOTAL_CLIENTS += 1

    # handle lefting clients
    def client_leave_event(self, addr, data):

        id = encryption_processing.decrypt(data).split(" : ")[1].split(" >> ")[0]

        self.clients_id.pop(self.clients_id.index(id))
        logging.log_online_users(self.clients_id)

        STATICS.TOTAL_CLIENTS -= 1

        self.clients.pop(self.clients.index(addr))
        for client in self.clients:
            self.s.sendto(encryption_processing.encrypt("[-] " + id + " is now offline"), client)

    # handle command requests
    def command_handler(self, client, data):

        command_request = encryption_processing.encrypt("[*] client command request : " +
               user_commands.commands(encryption_processing.decrypt(data).split(" >> ")[1].split(" ")[1]))
        self.s.sendto(command_request, client)

    # handle login request
    def login(self, client, data):

        print("\n[*] login request by " + str(client))

        recvd_id = str(encryption_processing.hash(encryption_processing.decrypt(data).split(" ")[0]))
        recvd_pwd = str(encryption_processing.hash(encryption_processing.decrypt(data).split(" ")[1]))

        try:
            d = database()
            if d.read_user(recvd_id, recvd_pwd):
                self.log_client(client, data)
                print("    -> login granted\n")
                self.s.sendto(encryption_processing.encrypt("granted"), client)
            else:
                print("    -> login denied\n")
                self.s.sendto(encryption_processing.encrypt("denied"), client)

        except Exception as e:
            print("[-] error cause: ", e)

    def signup(self, client, data):

        print("\n[*] sign up request by " + str(client) + "\n")

        register_id = str(encryption_processing.hash(encryption_processing.decrypt(data).split(".")[1].split(" ")[0]))
        register_pwd = str(encryption_processing.hash(encryption_processing.decrypt(data).split(".")[1].split(" ")[1]))

        try:
            d = database()
            d.add_user(register_id, register_pwd)

            # self.s.sendto(encryption_processing.encrypt("granted"), client)
            self.login(client, encryption_processing.encrypt(encryption_processing.decrypt(data).split(".")[1]))

        except Exception as e:
            print("[-] error cause: ", e, "\n")

    # run server
    def run_server(self):

        self.s.bind((self.SERVER_IP, self.PORT))
        self.s.setblocking(0)

        print("[*] server started")

        quitting = False

        while not quitting:
            try:
                data, addr = self.s.recvfrom(1024)

                print(time.ctime(time.time()) + str(addr) + " : " + encryption_processing.decrypt(data).split(" : ")[1])

                # sign up request
                if encryption_processing.decrypt(data).split(".")[0] == "r":
                    self.signup(addr, data)

                # login request
                elif encryption_processing.decrypt(data).split(" >> ")[1] == "status.set(online)":
                    self.login(addr, data)

                # commands request
                elif encryption_processing.decrypt(data).split(" >> ")[1].split(" ")[0] == "-c":
                    self.command_handler(addr, data)

                # client exit
                elif encryption_processing.decrypt(data).split(" >> ")[1] == "status.set(offline)":
                    self.client_leave_event(addr, data)

                # usual sending
                else:
                    for client in self.clients:
                        self.s.sendto(data, client)

            except:
                pass

        self.s.close()


server = server()
server.run_server()

