from dummy_data import insert_dummy_data
from registration import registration_menu
from manager_functions import manager_login
from driver_functions import driver_login
from client_functions import client_login
from utility import clear_terminal

# main menu #
def main_menu():
    while(True):
        print("MOBILITYMANAGER")
        print('---------------')
        print("1: Registration")
        print("2: Login")
        print("3: Exit Application")
        try:
            choice = int(input("Choice (1-3): "))
            clear_terminal()
            match choice:
                case 1: return "registration"
                case 2: return "login"
                case 3: return "exit"
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Enter a valid menu choice.")

# login menus
def login_menu():
    while(True):
        print("LOGIN")
        print('-----')
        print("1. Manager Login")
        print("2. Driver Login")
        print("3. Client Login")
        print("4. Back")
        try:
            choice = int(input("Choice (1-4): "))
            clear_terminal()
            match choice:
                case 1: manager_login()
                case 2: driver_login()
                case 3: client_login()
                case 4: break
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Invalid menu choice.")

# MAIN #
while True:
    action = main_menu()
    match action:
        case "registration": registration_menu()
        case "login": login_menu()
        case "exit": break