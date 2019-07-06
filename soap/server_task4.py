# first run python -m Pyro4.naming
# server side
import sqlite3
import os
import fnmatch
from spyne import Application, rpc, ServiceBase, Iterable, Unicode
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import json
sql_file = 'katanemimena.db'


def find_db(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


class ManagerClass(ServiceBase):

    @rpc(Unicode, _returns=Iterable(Unicode))
    def request_manager(ctx,data):
        database = DataBaseConnection()
        data = json.loads(data)
        type = data['type']
        if type == 'add':
            # response = self.add_contact(data['name'], data['email'], data['phone'])
            response = database.add_contact(data['name'], data['email'], data['phone'])
            yield json.dumps({'response': response})
        elif type == 'update':
            response = database.update_contact(data['contact_id'], data['name'], data['email'], data['phone'])
            yield json.dumps({'response': response})
        elif type == 'search':
            response = database.search_contact(data['search_value'])
            yield json.dumps({'response': response})
        elif type == 'delete':
            response = database.delete_contact(data['contact_id'])
            yield json.dumps({'response': response})


class DataBaseConnection:
    def __init__(self):
        self.__start_db()

    def __start_db(self):
        self.conn = sqlite3.connect(sql_file)
        self.c = self.conn.cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS CONTACTS
                   (ID INT PRIMARY KEY    NOT NULL,
                   NAME           TEXT    NOT NULL,
                   EMAIL          TEXT    NOT NULL,
                   PHONE_NUMBER   TEXT    NOT NULL);''')

        self.c.execute("select count(*) from CONTACTS")
        is_empty = self.c.fetchone()[0]

        if is_empty == 0:
            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                                      VALUES (1, 'Paul', 'temp1@gmail.com', 6979263755)")

            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                                      VALUES (2, 'Maria', 'temp2@gmail.com', 6979242156)")

            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                                      VALUES (3, 'John', 'temp3@gmail.com', 6987543245)")

            self.c.execute("INSERT INTO CONTACTS (ID,NAME,EMAIL,PHONE_NUMBER) \
                                      VALUES (4, 'Nick', 'temp4@gmail.com', 6978432421)")
            self.conn.commit()

    def add_contact(self, name, email, phone):
        try:
            self.c.execute("select count(*) from CONTACTS")
            max_id = self.c.fetchone()[0] + 1
            self.c.execute("INSERT INTO CONTACTS VALUES (?,?,?,?)", (max_id, name, email, phone))
            self.conn.commit()
        except:
            return 'Something went wrong. Try again'
        return 'Add done'

    def update_contact(self, contact_id, name, email, phone):
        try:
            self.c.execute("""UPDATE CONTACTS SET name = ?, EMAIL = ?, PHONE_NUMBER = ? WHERE ID=? """, \
                       (name, email, phone, contact_id))
            self.conn.commit()
        except:
            return 'Something went wrong. Try again'
        return 'Update done'

    def search_contact(self, search_value):
        final_search_value = '%' + search_value + '%'
        self.c.execute("""SELECT * FROM CONTACTS WHERE NAME like ? or EMAIL like ? or PHONE_NUMBER like ? """, \
                       (final_search_value, final_search_value, final_search_value))
        results = self.c.fetchall()
        return results

    def delete_contact(self,contact_id):
        try:
            self.c.execute('''DELETE FROM CONTACTS where ID =? ''', (contact_id))
        except:
            return 'Something went wrong. Try again'
        self.conn.commit()
        return 'Delete done'


application = Application([ManagerClass], 'spyne.database_connection.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)

if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://127.0.0.1:8000")
    logging.info("wsdl is at: http://localhost:8000/?wsdl")

    server = make_server('127.0.0.1', 8000, wsgi_application)
    server.serve_forever()
