# client side
import Pyro4

connection_with_server = Pyro4.Proxy("PYRONAME:HM1")

print('Hello')

while True:
    print('Choose 1 in order to add a new contact ')
    print('Choose 2 in order to update a contact ')
    print('Choose 3 in order to search for a contact ')
    print('Choose 4 in order to delete a contact ')
    print('Choose 5 if you want to leave \n')
    user_selection = int(input())

    if user_selection == 1:
        name = input('Give name : ')
        email = input('Give email : ')
        phone = input('Give phone number : ')
        print(connection_with_server.add_contact(name, email, phone))
    elif user_selection == 2:
        contact_id = input('Give contact\'s id that you cant to modify : ')
        name = input('Give name : ')
        email = input('Give email : ')
        phone = input('Give phone number : ')
        print(connection_with_server.update_contact(contact_id, name, email, phone))
    elif user_selection == 3:
        print('You can search every value at every column')
        search_value = input('Give value that you want to search : \n')
        results = connection_with_server.search_contact(search_value)
        [print(' '.join(map(str, item))) for item in results]
    elif user_selection == 4:
        contact_id = input('Give contact\'s id that you want to delete')
        print(connection_with_server.delete_contact(contact_id))
    elif user_selection == 5:
        break
    else:
        print('Wrong input, try again')

print('Goodbye')
