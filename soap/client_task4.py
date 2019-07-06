# client side
from zeep import Client
import json

client = Client('http://localhost:8000/?wsdl')
# print (hello_client.service.say_hello(data, 10))
print('Hello')

while True:
    print('Choose 1 in order to add a new contact ')
    print('Choose 2 in order to update a contact ')
    print('Choose 3 in order to search for a contact ')
    print('Choose 4 in order to delete a contact ')
    print('Choose 5 if you want to leave\n')
    user_selection = int(raw_input())

    if user_selection == 1:
        name = raw_input('Give name : ')
        email = raw_input('Give email : ')
        phone = raw_input('Give phone number : ')
        message = json.dumps({'name': name, 'email': email, 'phone': phone, 'type': 'add'})
        response = client.service.request_manager(message)
        response = json.loads(response[0])
        response = response['response'].encode('ascii','ignore')
        print(response)
    elif user_selection == 2:
        contact_id = raw_input('Give contact\'s id that you cant to modify : ')
        name = raw_input('Give name : ')
        email = raw_input('Give email : ')
        phone = raw_input('Give phone number : ')
        message = json.dumps({'contact_id':contact_id, 'name': name, 'email': email, 'phone': phone, 'type': 'update'})
        response = client.service.request_manager(message)
        response = json.loads(response[0])
        response = response['response'].encode('ascii', 'ignore')
        print(response)
    elif user_selection == 3:
        print('You can search every value at every column')
        search_value = raw_input('Give value that you want to search : \n')
        message = json.dumps({'search_value':search_value, 'type': 'search'})
        response = client.service.request_manager(message)
        response = json.loads(response[0])
        response = response['response'][0]
        temp_message = [str(item) for item in response]
        response_to_show = ' '.join(temp_message)
        print(response_to_show)
    elif user_selection == 4:
        contact_id = raw_input('Give contact\'s id that you want to delete')
        message = json.dumps({'contact_id': contact_id, 'type': 'delete'})
        response = client.service.request_manager(message)
        response = json.loads(response[0])
        response = response['response'].encode('ascii', 'ignore')
        print(response)
        print(response_to_show)
    elif user_selection == 5:
        break
    else:
        print('Wrong raw_input, try again')

print('Goodbye')
