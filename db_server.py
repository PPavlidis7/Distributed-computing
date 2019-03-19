# first run python -m Pyro4.naming
# server side
import sqlite3
import os
import fnmatch
import Pyro4

sql_file = 'katanemimena.db'

def find_db(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


@Pyro4.expose
class DataBaseConnection(object):
    def __init__(self):
        self.__start_db()

    def __start_db(self):

        # check if db exist. If not create it
        if len(find_db('*.db', './')) > 0:
            self.conn = sqlite3.connect(sql_file)
            self.c = self.conn.cursor()
        else:
            self.conn = sqlite3.connect(sql_file)
            self.c = self.conn.cursor()
            self.c.execute('''CREATE TABLE CONTACTS
                     (ID INT PRIMARY KEY    NOT NULL,
                     NAME           TEXT    NOT NULL,
                     EMAIL          TEXT    NOT NULL,
                     PHONE_NUMBER   TEXT    NOT NULL);''')

            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (1, 'Paul', 'temp1@gmail.com', 6979263755)")

            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (2, 'Maria', 'temp2@gmail.com', 6979242156)")

            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (3, 'John', 'temp3@gmail.com', 6987543245)")

            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (4, 'Nick', 'temp4@gmail.com', 6978432421)")
            self.conn.commit()

        # temp = self.conn.sqlExec('SELECT COUNT(*) * FROM {tn}'.format(tn=table_name))
        temp = self.c.execute("select * from CONTACTS where id ==1")
        print("->", len(temp.fetchall()), temp.fetchall())

    def add_contact(self, name,email,phone):
        self.c.execute("INSERT INTO CONTACTS VALUES (NULL,?,?,?)", (name,email,phone))

    def update_contact(self):
        self.x = 0

    def search_contact(self):
        self.x = 0

    def delete_contact(self):
        self.x = 0


if __name__ == '__main__':
    x = DataBaseConnection()
    daemon = Pyro4.Daemon()  # make a Pyro daemon
    ns = Pyro4.locateNS()  # find the name server
    uri = daemon.register(DataBaseConnection)  # register the greeting maker as a Pyro object
    ns.register("HM1", uri)  # register the object with a name in the name server
    print("Ready.")
    daemon.requestLoop()  # start the event loop of the server to wait for calls
