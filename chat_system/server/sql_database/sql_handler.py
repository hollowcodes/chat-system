import sqlite3


class database:

    def __init__(self):

        self.connect = sqlite3.connect(r"\user_register.db")
        self.cursor = self.connect.cursor()
    
    def create_register_table(self):
    
        self.cursor.execute("""CREATE TABLE register (
                        username text,
                        password text)""")
    
        self.connect.commit()
        self.connect.close()

        print("[*] new sql table created")
    
    def add_user(self, id, pwd):
        self.cursor.execute("INSERT INTO register VALUES (?,?)", (id, pwd))
    
        self.connect.commit()
        self.connect.close()

        print("[*] new entry created: ('" + id + "', '" + pwd + "')\n")
    
    def read_user(self, id, pwd):

        try:
            self.cursor.execute("SELECT * FROM register WHERE username=? AND password=?", (id, pwd))

            r = self.cursor.fetchall()

            self.connect.commit()
            self.connect.close()

            if len(r) == 0:
                print("[-] there is no database entry like ('" + id + "', '" + pwd + "')")

                return False

            elif len(r) > 0:
                return True

            else:
                print("[-] sql error!")

        except Exception as e:
            print("[-] error cause: ", e)


# d = database()

# d.add_user(id, pwd)

# d.read_user(id, pwd)

# d.create_register_table()

