# server side
import sqlite3
import os
import fnmatch
import pika
import json

sql_file = 'katanemimena.db'


def find_db(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result


class DataBaseConnection:
    def __init__(self):
        self.__start_db()
        print(" [x] Awaiting RPC requests")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host='172.17.0.3'))
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='add')
        self.channel.queue_declare(queue='update')
        self.channel.queue_declare(queue='search')
        self.channel.queue_declare(queue='delete')

        self.channel.basic_consume(self.add_contact, 'add')
        self.channel.basic_consume(self.update_contact, 'update')
        self.channel.basic_consume(self.search_contact, 'search')
        self.channel.basic_consume(self.delete_contact, 'delete')

        self.channel.start_consuming()

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

    def add_contact(self, ch, method, props, body):
        print "user call add"
        data = json.loads(body)
        name = data["name"]
        email = data["email"]
        phone = data["phone"]
        try:
            self.c.execute("select count(*) from CONTACTS")
            max_id = self.c.fetchone()[0] + 1
            self.c.execute("INSERT INTO CONTACTS VALUES (?,?,?,?)", (max_id, name, email, phone))
            self.conn.commit()
            response = 'Add done'
        except:
            response = 'Something went wrong. Try again'

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id= props.correlation_id),
                         body=json.dumps({'data':response}))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def update_contact(self, ch, method, props, body):
        print "user call update"
        data = json.loads(body)
        contact_id = data['contact_id']
        name = data['name']
        email = data['email']
        phone = data['phone']
        try:
            self.c.execute("""UPDATE CONTACTS SET name = ?, EMAIL = ?, PHONE_NUMBER = ? WHERE ID=? """, \
                       (name, email, phone, contact_id))
            self.conn.commit()
            response = 'Update done'
        except:
            response = 'Something went wrong. Try again'

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps({'data':response}))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def search_contact(self, ch, method, props, body):
        print "user call search"
        data = json.loads(body)
        search_value = data['search_value']
        final_search_value = '%' + search_value + '%'
        self.c.execute("""SELECT * FROM CONTACTS WHERE NAME like ? or EMAIL like ? or PHONE_NUMBER like ? """, \
                       (final_search_value, final_search_value, final_search_value))
        results = self.c.fetchall()
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps({'data':results}))
        ch.basic_ack(delivery_tag=method.delivery_tag)

    def delete_contact(self,ch, method, props, body):
        print "user call delete"
        data = json.loads(body)
        contact_id = data["contact_id"]
        try:
            self.c.execute('''DELETE FROM CONTACTS where ID =? ''', (contact_id))
            response = 'Delete done'
        except:
            response = 'Something went wrong. Try again'

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps({'data':response}))
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    server = DataBaseConnection()
