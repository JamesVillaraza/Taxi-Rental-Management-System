from utility import clear_terminal, update_table, execute_query

def driver_login():
    sql_query = """SELECT name FROM driver"""
    driver_names = [x[0] for x in execute_query(sql_query)]
    print(driver_names)

    print("DRIVER LOGIN")
    print("------------")
    driver_name = input("Enter Driver Name to login (case-sensitive): ")

    clear_terminal()

    if driver_name not in driver_names:
        print("Invalid Driver Login... returning to login menu.")
        return

    # at this point we are logged in
    driver_menu(driver_name)

def driver_menu(driver_name):
    while(True):
        print(f"DRIVER MENU -- {driver_name}")
        print('---------------' + ('-' * len(driver_name)))
        print("1. Change Address")
        print("2. Declare & List Car Models")
        print("3. Logout")
        try:
            choice = int(input("Choice (1-3): "))
            clear_terminal()
            match choice:
                case 1: change_driver_address(driver_name)
                case 2: manage_driver_models(driver_name)
                case 3: break
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Invalid menu choice.")

def change_driver_address(driver_name):
    print("CHANGE ADDRESS")
    print("--------------")

    # Get new address info
    try:
        address_number = int(input("Enter new Address Number: ").strip())
        road_name = input("Enter new Road Name: ").strip()
        city = input("Enter new City: ").strip()

        # You might want to clear the terminal after taking input
        clear_terminal()

        # First, insert the new address if it doesn't already exist
        sql_insert_address = f"""
            INSERT INTO Address (roadName, addressNumber, city)
            VALUES ('{road_name}', {address_number}, '{city}')
            ON CONFLICT DO NOTHING;
        """
        update_table(sql_insert_address)

        # Now update the driver's address
        sql_update_driver = f"""
            UPDATE Driver
            SET addressNumber = {address_number},
                roadName = '{road_name}',
                city = '{city}'
            WHERE name = '{driver_name}';
        """
        update_table(sql_update_driver)
        clear_terminal()
        print(f"Address updated successfully for {driver_name}!")
    except ValueError:
        clear_terminal()
        print("Invalid address number, must be an integer. Returning to menu.")
        return

def manage_driver_models(driver_name):
    while True:
        print("DRIVER MODEL MANAGEMENT")
        print("-------------------------")
        print("1. View all car models")
        print("2. View models you can drive")
        print("3. Declare a model you can drive")
        print("4. Remove a model you no longer drive")
        print("5. Exit")
        choice = input("Enter choice: ").strip()

        clear_terminal()

        if choice == '1':
            view_car_models()
        elif choice == '2':
            view_driver_models(driver_name)
        elif choice == '3':
            declare_model(driver_name)
        elif choice == '4':
            remove_model(driver_name)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please select a valid option.")

        input("\nPress Enter to continue...")
        clear_terminal()

def view_car_models():
    sql_view_models = """
        SELECT constructionYear, brand, transmission, color, model.carId, modelId
        FROM Model
        JOIN Car ON Model.carId = Car.carId
    """
    models = execute_query(sql_view_models)
    print(f"{'Year':<8} {'Brand':<10} {'Transmission':<14} {'Color':<10} {'CarID':<8} {'ModelID':<8}")
    print("-" * 62)
    for year, brand, transmission, color, carid, modelid in models:
        print(f"{year:<8} {brand:<10} {transmission:<14} {color:<10} {carid:<8} {modelid:<8}")

def view_driver_models(driver_name):
    sql_driver_models = f"""
        SELECT constructionYear, brand, transmission, color, drives.carId, drives.modelId
        FROM Drives
        JOIN Model ON Drives.modelId = Model.modelId AND Drives.carId = Model.carId
        JOIN Car ON Drives.carId = Car.carId
        WHERE name = '{driver_name}'
    """
    driver_models = execute_query(sql_driver_models)
    if not driver_models:
        print("You have not declared any car models yet.")
    else:
        print(f"\n{'Year':<8} {'Brand':<10} {'Trans.':<12} {'Color':<10} {'CarID':<8} {'ModelID':<8}")
        print("-" * 60)
        for year, brand, transmission, color, carid, modelid in driver_models:
            print(f"{year:<8} {brand:<10} {transmission:<12} {color:<10} {carid:<8} {modelid:<8}")

def declare_model(driver_name):
    print("All Car Models")
    print('-'*62)
    view_car_models()
    print('-'*62)
    try:
        # Get user input for CarID and ModelID
        carid = int(input("Enter CarID you can drive: ").strip())
        modelid = int(input("Enter ModelID you can drive: ").strip())

        # Validate if CarID exists
        sql_validate_car = f"SELECT carid FROM car WHERE carid = {carid};"
        car_exists = execute_query(sql_validate_car)
        
        # Validate if ModelID exists
        sql_validate_model = f"SELECT modelid FROM model WHERE modelid = {modelid} AND carid = {carid};"
        model_exists = execute_query(sql_validate_model)

        if not car_exists:
            print(f"Error: CarID {carid} does not exist.")
        elif not model_exists:
            print(f"Error: ModelID {modelid} does not exist for CarID {carid}.")
        else:
            # Check if the driver already drives this car model
            sql_check_driver = f"""
                SELECT * FROM drives 
                WHERE name = '{driver_name}' AND modelid = {modelid} AND carid = {carid};
            """
            existing_drive = execute_query(sql_check_driver)
            
            if existing_drive:
                print(f"Error: You are already declared as a driver for CarID {carid}, ModelID {modelid}.")
            else:
                # If the driver is not already driving the car, insert the new record
                sql_insert_drive = f"""
                    INSERT INTO drives (name, modelid, carid) 
                    VALUES ('{driver_name}', {modelid}, {carid});
                """
                update_table(sql_insert_drive)
                print(f"Successfully declared CarID {carid}, ModelID {modelid} as a car model you can drive.")

    except ValueError:
        print("Error: CarID and ModelID must be numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")

def remove_model(driver_name):
    # Check if the driver has any declared car models
    sql_check_driver_models = f"""
        SELECT COUNT(*) FROM drives
        WHERE name = '{driver_name}';
    """
    driver_models_count = execute_query(sql_check_driver_models)[0][0]  # Extract the count

    if driver_models_count == 0:
        clear_terminal()
        print(f"{driver_name} has no declared car models to remove.")
        return  # Exit the function if no models are declared

    print(f"{driver_name}'s DECLARED CAR MODELS")
    print('-' * 62)
    view_driver_models(driver_name)  # Display all declared models
    print('-' * 62)
    
    try:
        carid = int(input("Enter CarID you no longer drive: ").strip())
        modelid = int(input("Enter ModelID you no longer drive: ").strip())

        # Perform the deletion of the driver's declared model
        sql_delete_drive = f"""
            DELETE FROM Drives
            WHERE name = '{driver_name}' AND modelId = {modelid} AND carId = {carid}
        """
        update_table(sql_delete_drive)
        clear_terminal()
        print("Successfully removed car model!")

    except ValueError:
        clear_terminal()
        print("CarID and ModelID must be numbers. Please try again.")
    except Exception as e:
        clear_terminal()
        print(f"An error occurred: {e}")