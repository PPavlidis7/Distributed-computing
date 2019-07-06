# client side
# need to run: pip install -r requirements.txt
import json
import requests
import ast


print('Hello')

while True:
    print('Choose 1 in order to add a new contact ')
    print('Choose 2 in order to update a contact ')
    print('Choose 3 in order to search for a contact ')
    print('Choose 4 in order to delete a contact ')
    print('Choose 5 if you want to leave \n')
    user_selection = int(input())

    if user_selection == 1:
        name = raw_input('Give name : ')
        email = raw_input('Give email : ')
        phone = raw_input('Give phone number : ')
        message = json.dumps({'name': name, 'email': email, 'phone': phone})
        r = requests.post("http://127.0.0.1:5000/add", data=message)
        response = json.loads(r.content)
        response_message = response['message']
        print response_message
    elif user_selection == 2:
        contact_id = input('Give contact\'s id that you cant to modify : ')
        name = raw_input('Give name : ')
        email = raw_input('Give email : ')
        phone = raw_input('Give phone number : ')
        message = json.dumps({'name': name, 'email': email, 'phone': phone,
                              'contact_id' : contact_id})
        r = requests.put("http://127.0.0.1:5000/update", data=message)
        response = json.loads(r.content)
        response_message = response['message']
        print response_message
    elif user_selection == 3:
        print('You can search every value at every column')
        search_value = raw_input('Give value that you want to search : \n')
        r = requests.get("http://127.0.0.1:5000/search/" + search_value)
        response = json.loads(r.content)
        response = ast.literal_eval(json.dumps(response))
        response_message = response['message']
        print response_message
    elif user_selection == 4:
        contact_id = raw_input('Give contact\'s id that you want to delete : ')
        r = requests.delete("http://127.0.0.1:5000/delete/" + contact_id)
        response = json.loads(r.content)
        response_message = response['message']
        print response_message

    elif user_selection == 5:
        break
    else:
        print('Wrong input, try again')

print('Goodbye')
