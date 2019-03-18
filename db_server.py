
import sqlite3
import os
import fnmatch
import Pyro4


@Pyro4.expose
class DataBaseConnection(object):
    def __init__(self):
        self.__start_db()

    def __find(self, pattern, path):
        result = []
        for root, dirs, files in os.walk(path):
            for name in files:
                if fnmatch.fnmatch(name, pattern):
                    result.append(os.path.join(root, name))
        return result

    def __start_db(self):
        self.conn = sqlite3.connect('katanemimena.db')

        #chech if db existis. If not create it
        if len(self.__find('*.db', './')) >0:
            pass
        else:
            self.conn.execute('''CREATE TABLE CONTACTS
                     (ID INT PRIMARY KEY    NOT NULL,
                     NAME           TEXT    NOT NULL,
                     EMAIL          TEXT    NOT NULL,
                     PHONE_NUMBER         TEXT    NOT NULL);''')

            self.conn.execute("INSERT INTO contacts (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (1, 'Paul', 'temp1@gmail.com', 6979263755)")

            self.conn.execute("INSERT INTO contacts (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (2, 'Maria', 'temp2@gmail.com', 6979242156)")

            self.conn.execute("INSERT INTO contacts (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (3, 'John', 'temp3@gmail.com', 6987543245)")

            self.conn.execute("INSERT INTO contacts (ID,NAME,EMAIL,PHONE_NUMBER) \
                          VALUES (4, 'Nick', 'temp4@gmail.com', 6978432421)")
            self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    daemon = Pyro4.Daemon()  # make a Pyro daemon
    ns = Pyro4.locateNS()  # find the name server
    uri = daemon.register(DataBaseConnection)  # register the greeting maker as a Pyro object
    ns.register("HM1", uri)  # register the object with a name in the name server
    print("Ready.")
    daemon.requestLoop()  # start the event loop of the server to wait for calls
