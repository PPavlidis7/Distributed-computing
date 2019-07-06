# server side
# need to run: pip install -r requirements.txt
import sqlite3
import os
import fnmatch
import json
import ast
from flask import Flask, request, json, make_response
from flask_classful import FlaskView, route

app = Flask(__name__)
sql_file = 'katanemimena.db'


def find_db(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


def output_json(data, code, headers=None):
    content_type = 'application/json'
    dumped = json.dumps(data)
    if headers:
        headers.update({'Content-Type': content_type})
    else:
        headers = {'Content-Type': content_type}
    response = make_response(dumped, code, headers)
    return response


class DataBaseConnection(FlaskView):
    representations = {'application/json': output_json}

    def __init__(self):
        self.__start_db()
        print("Ready")

    def __start_db(self):
        self.conn = sqlite3.connect(sql_file, check_same_thread=False)
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

    @route('/add', methods=['POST'])
    def add_contact(self):
        data = json.loads(request.data)
        data = ast.literal_eval(json.dumps(data))
        name, email, phone = data["name"], data["email"], data["phone"]
        try:
            self.c.execute("select count(*) from CONTACTS")
            max_id = self.c.fetchone()[0] + 1
            self.c.execute("INSERT INTO CONTACTS VALUES (?,?,?,?)", (max_id, name, email, phone))
            self.conn.commit()
        except:
            return {'message': 'Something went wrong. Try again'}, 404
        return {'message': 'Add done'}, 200

    @route('/update', methods=['PUT'])
    def update_contact(self):
        data = json.loads(request.data)
        data = ast.literal_eval(json.dumps(data))
        name, email, phone, contact_id = data["name"], data["email"], data["phone"], data['contact_id']
        try:
            self.c.execute("""UPDATE CONTACTS SET name = ?, EMAIL = ?, PHONE_NUMBER = ? WHERE ID=? """, \
                       (name, email, phone, contact_id))
            self.conn.commit()
        except:
            return {'message': 'Something went wrong. Try again'}, 404
        return {'message': 'Update done'}, 200

    @route('/search/<search_value>')
    def search_contact(self, search_value):
        final_search_value = '%' + search_value + '%'
        self.c.execute("""SELECT * FROM CONTACTS WHERE NAME like ? or EMAIL like ? or PHONE_NUMBER like ? """, \
                       (final_search_value, final_search_value, final_search_value))
        results = self.c.fetchall()
        if len(results):
            temp = {'message': results[0]}
            response = ast.literal_eval(json.dumps(temp))
            return response, 200
        else:
            return {'message': 'Could not found given registry'}, 200

    @route('/delete/<contact_id>', methods=['DELETE'])
    def delete_contact(self, contact_id):
        try:
            self.c.execute('''DELETE FROM CONTACTS where ID =? ''', (contact_id))
        except:
            return {'message': 'Something went wrong. Try again'}, 404
        self.conn.commit()
        return {'message': 'Delete done'}, 200


if __name__ == '__main__':
    DataBaseConnection.register(app, route_base="/")
    app.run()
