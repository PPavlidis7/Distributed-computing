# client side
import Pyro4

connection_with_server = Pyro4.Proxy("PYRONAME:HM1")

print('Hello')

while True:
    print('Choose 1 in order to add a new contact ')
    print('Choose 2 in order to update a contact ')
    print('Choose 3 in order to search for a contact ')
    print('Choose 4 in order to delete a contact ')
    print('Choose 5 if you want to leave ')
    user_selection = int(input())

    if user_selection == 1:
        name = input('Give name : ')
        email = input('Give email : ')
        phone = input('Give phoner number : ')
        connection_with_server.add_contact(name,email,phone)
    if user_selection == 2:
        pass
    if user_selection == 3:
        pass
    if user_selection == 4:
        pass
    if user_selection == 5:
        break
    else:
        print('Wrong input, try again')

print('Goodbye')
