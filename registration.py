from utility import clear_terminal, update_table, cursor
import checker

# registration menus #
def registration_menu():
    while(True):
        print("REGISTRATION")
        print('------------')
        print("1. Register Manager")
        print("2. Register Client")
        print("3. Back")
        try:
            choice = int(input("Choice (1-3): "))
            clear_terminal()
            match choice:
                case 1: register_manager()
                case 2: register_client()
                case 3: break
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Invalid menu choice.")

# TODO:
# might want to implement some way for the user to quit this registration screen by typing in "quit" or something
def register_manager():
    print("MANAGER REGISTRATION")
    print('--------------------')
    print("(Type 'quit' at any time to cancel.)")

    name = input("Enter Name: ").strip()
    if name.lower() == 'quit':
        clear_terminal()
        print("Registration cancelled.")
        return

    while True:
        ssn_input = input("Enter SSN: ").strip()
        if ssn_input.lower() == 'quit':
            clear_terminal()
            print("Registration cancelled.")
            return
        try:
            ssn = int(ssn_input)
            if checker.check_exisiting_mngrssn(ssn, cursor):
                clear_terminal()
                print(f"{ssn} already exists... returning to registration.")
                return
            break
        except ValueError:
            clear_terminal()
            print(f"{ssn_input} is an invalid SSN, needs to be a number.")
            return

    email = input("Enter Email: ").strip()
    if email.lower() == 'quit':
        clear_terminal()
        print("Registration cancelled.")
        return

    sql_insert_manager = f"""  
        INSERT INTO Manager (ssn, name, email) VALUES
        ({ssn}, '{name}', '{email}');
    """
    update_table(sql_insert_manager)


def register_client():
    print("CLIENT REGISTRATION")
    print('-------------------')
    name = input("Enter Name: ")
    email = input("Enter Email: ")
    if checker.check_exisiting_email(email, cursor) == True:
        clear_terminal()
        print(f"{email} already exists... returning to registration.")
        return

    sql_insert_client = f"""  
        INSERT INTO client (name, email) VALUES
        ('{name}', '{email}');
    """
    update_table(sql_insert_client)

    while(True):
        print("ENTER ADDRESS OR CREDIT CARD")
        print('----------------------------')
        print("1. Address Entry")
        print("2. Credit Card Entry")
        print("3. Done")
        try:
            choice = int(input("Choice (1-3): "))
            clear_terminal()
            match choice: 
                case 1: enter_address(email)
                case 2: enter_credit_card(email)
                case 3: break
                case _: raise ValueError
        except ValueError:
                clear_terminal()
                print("Invalid menu choice.")

def enter_address(email):
    print("ADDRESS ENTRY")
    print('-------------')
    roadname = input("Enter road name: ")
    try:
        addressnum = int(input("Enter address number: "))
    except ValueError as ve:
        clear_terminal()
        print(f"{ve} is an invalid address number, needs to be a number.")
        return
    city = input("Enter city: ")
    result = checker.check_existing_address((roadname, addressnum, city), cursor)
    if result[0] == False:
        print(f"{addressnum} {roadname}, {city} doesn't exist.")
        choice = input("Add it to the Address table? (1. Yes, 2. No): ")
        while(choice != '1' or choice != '2'):
            match choice:
                case '1': break
                case '2': 
                    print(f"{addressnum} {roadname}, {city} not added.")
                    clear_terminal() 
                    return
                case _: 
                    clear_terminal()
                    print('Invalid choice, try Again.')
                    choice = input(f"Add {addressnum} {roadname}, {city} to the Address table? (1. Yes, 2. No): ")

        #  insert into Address table because the address doesn't exist where the client is entering
        sql_insert_address = f"""
            INSERT INTO address (roadname, addressnumber, city) VALUES
            ('{roadname}', {addressnum}, '{city}')
        """
        update_table(sql_insert_address)
    else: # address exists, just set it equal to the result for case-sensitivity
        roadname = result[1][0]
        addressnum = result[1][1]
        city = result[1][2]
    # insert in staysAt
    sql_insert_staysAt = f"""
            INSERT INTO staysat (roadname, addressnumber, city, email) VALUES
            ('{roadname}', {addressnum}, '{city}', '{email}')
        """
    update_table(sql_insert_staysAt)

def enter_credit_card(email):
    print("CREDIT CARD ENTRY")
    print('-----------------')
    # enter card number
    try: 
        cardnum = int(input("Enter Credit Card Number: "))
        if checker.check_existing_card(cardnum, cursor) == True:
            clear_terminal()
            print(f"{cardnum} already exists... returning to address/card entry.")
            return 
    except ValueError as ve:
        clear_terminal()
        print(f"{ve} is an invalid credit card number, needs to be a number.")
        return
    
    # payment address entry
    roadname = input("Enter payment road name: ")
    try:
        addressnum = int(input("Enter payment address number: "))
    except ValueError as ve:
        clear_terminal()
        print(f"{ve} is an invalid address number, needs to be a number.")
        return
    city = input("Enter payment city: ")
    result = checker.check_existing_address((roadname, addressnum, city), cursor)
    if result[0] == False:
        print(f"{addressnum} {roadname}, {city} doesn't exist.")
        choice = input("Add it to the Address table? (1. Yes, 2. No): ")
        while(choice != '1' or choice != '2'):
            match choice:
                case '1': break
                case '2':
                    clear_terminal()
                    print(f"{addressnum} {roadname}, {city} not added.")
                    return
                case _: 
                    clear_terminal()
                    print('Invalid choice, try Again.')
                    choice = input(f"Add {addressnum} {roadname}, {city} to the Address table? (1. Yes, 2. No): ")

        #  insert into Address table because the payment address client entered doesn't exist
        sql_insert_address = f"""
            INSERT INTO address (roadname, addressnumber, city) VALUES
            ('{roadname}', {addressnum}, '{city}')
        """
        update_table(sql_insert_address)
    else: # address exists, just set it equal to the result for case-sensitivity
        roadname = result[1][0]
        addressnum = result[1][1]
        city = result[1][2]
    # insert in credit card
    sql_insert_cardnum = f"""
            INSERT INTO creditcard (creditcardnumber, email, addressnumber, roadname, city) VALUES
            ({cardnum}, '{email}', {addressnum}, '{roadname}', '{city}')
        """
    update_table(sql_insert_cardnum)

#############################################