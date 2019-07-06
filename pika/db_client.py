# client side
import pika
import uuid
import json

class ClientSide(object):
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='172.17.0.3'))

        self.channel = self.connection.channel()

        result = self.channel.queue_declare('', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(self.on_response, queue=self.callback_queue,)

        self.__start_user_menu()

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def add(self, mesage):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='add',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=mesage)
        while self.response is None:
            self.connection.process_data_events()

    def update(self, mesage):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='update',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=mesage)
        while self.response is None:
            self.connection.process_data_events()

    def search(self, mesage):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='search',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=mesage)
        while self.response is None:
            self.connection.process_data_events()

    def delete(self, mesage):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key='delete',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=mesage)
        while self.response is None:
            self.connection.process_data_events()

    def __start_user_menu(self):
        print('Hello')

        while True:
            print('Choose 1 in order to add a new contact ')
            print('Choose 2 in order to update a contact ')
            print('Choose 3 in order to search for a contact ')
            print('Choose 4 in order to delete a contact ')
            print('Choose 5 if you want to leave \n')
            user_selection = int(raw_input())

            if user_selection == 1:
                name = raw_input('Give name : ')
                email = raw_input('Give email : ')
                phone = raw_input('Give phone number : ')
                message = json.dumps({'name': name, 'email': email, 'phone': phone})
                self.add(message)
                response = json.loads(self.response)
                response_data = response['data']
                print(response_data)

            elif user_selection == 2:
                contact_id = raw_input('Give contact\'s id that you cant to modify : ')
                name = raw_input('Give name : ')
                email = raw_input('Give email : ')
                phone = raw_input('Give phone number : ')
                temp_message = {}
                temp_message['name'] = name
                temp_message['email'] = email
                temp_message['phone'] = phone
                temp_message['contact_id'] = contact_id
                message = json.dumps(temp_message)
                self.update(message)
                print(self.response)

            elif user_selection == 3:
                print('You can search every value at every column')
                search_value = raw_input('Give value that you want to search : \n')
                temp_message = {}
                temp_message['search_value'] = search_value
                message = json.dumps(temp_message)
                self.search(message)
                response = json.loads(self.response)
                response_data = response['data']
                response_to_show = ''
                for item in response_data:
                    response_to_show= ' '.join(map(str, item))
                print(response_to_show)

            elif user_selection == 4:
                contact_id = raw_input('Give contact\'s id that you want to delete : ')
                temp_message = {}
                temp_message['contact_id'] = contact_id
                message = json.dumps(temp_message)
                self.delete(message)
                print(self.response)

            elif user_selection == 5:
                break
            else:
                print('Wrong raw_input, try again')
        print('Goodbye')


if __name__ == '__main__':
    client = ClientSide()
