import socket
import threading
import time
import sys

from chat_system.client import encryption_processing
from chat_system.client import STATICS


class client:

    def __init__(self):
        self.HOST_IP = STATICS.CLIENT_IP
        self.SERVER_IP = STATICS.SERVER_IP
        self.PORT = STATICS.PORT
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.register_prefix = ""

    def registry(self):
        print("\n[*] client started", STATICS.SERVER_IP)

        delimitation = "__________________________________"

        while True:
            print(delimitation + "\n")
            choice = input("[1] login\n[2] sign up\n>> ")

            if choice == "1":
                print(delimitation)
                print("\n[login]\n")
                id = input("username: ")
                pwd = input("password: ")

                print(delimitation + "\n")

                break

            elif choice == "2":
                print(delimitation)
                print("\n[register]\n")
                id = input("create.username: ")
                pwd = input("create.password: ")
                confim = input("confirm.password: ")

                if pwd == confim:
                    print(delimitation + "\n")

                    self.register_prefix = "r."

                    break

                else:
                    print("\n[-] wrong confirmation password\n")

            else:
                print("\n[-] choose login [1] or sign up [2]\n")
            
        return id, pwd

    def run_client(self):

        tLock = threading.Lock()
        shutdown = False

        def receving(name, sock, id):
            while not shutdown:
                try:
                    tLock.acquire()
                    while True:
                        data, addr = sock.recvfrom(1024)
                        if encryption_processing.decrypt(data) == "granted":
                            print("[+] granted, logged in as " + id + "\n")

                        elif encryption_processing.decrypt(data) == "denied":
                            print("[-] wrong login data\n")
                            exit(0)
                        else:
                            print(encryption_processing.decrypt(data) + "\n" + "write: ")
                except:
                    pass
                finally:
                    tLock.release()

        server = (self.SERVER_IP, self.PORT)

        self.s.bind((self.HOST_IP, 0))
        self.s.setblocking(0)

        id, pwd = self.registry()

        rT = threading.Thread(target=receving, args=("RecvThread", self.s, id))
        rT.start()

        self.s.sendto(
            encryption_processing.encrypt(self.register_prefix + id + " " + pwd + " (time.ctime(time.time()) : request by " + self.HOST_IP +
                                          " >> status.set(online)"), server)
        time.sleep(1)

        msg = input("write: ")

        while msg != "q":

            if msg != "":
                if msg == "exit":
                    self.s.sendto(
                        encryption_processing.encrypt(time.ctime(time.time()) + " : " + id + " >> status.set(offline)"), server)
                    sys.exit("[-] exit the client, socket closed")

                else:
                    self.s.sendto(encryption_processing.encrypt(time.ctime(time.time()) + " : " + id + " >> " + msg), server)

            msg = input("")

            tLock.acquire()
            tLock.release()

            time.sleep(0.2)

        rT.join()
        self.s.close()


c = client()
c.run_client()





