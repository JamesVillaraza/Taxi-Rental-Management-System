from utility import clear_terminal, update_table, execute_query

def manager_login():
    sql_query = """SELECT ssn FROM manager"""
    manager_ssns = [x[0] for x in execute_query(sql_query)]
    print("MANAGER LOGIN")
    print("-------------")
    try:
        ssn = int(input("Enter SSN to login: "))
        clear_terminal()
        if ssn not in manager_ssns: raise ValueError
    except ValueError as ve:
        clear_terminal()
        print("Invalid SSN Login... returning to login menu.")
        return
    
    # at this point we are logged in
    manager_menu(ssn)

def manager_menu(ssn):
    sql_query = f"""SELECT name FROM manager WHERE ssn = {ssn}"""
    manager_name = execute_query(sql_query)
    while(True):

        print(f"MANAGER MENU -- {manager_name}")
        print('-------------------------------')
        print("1. List & Manage Cars")
        print("2. Manage Drivers")
        print("3. Top Clients Report")
        print("4. Driver Statistics")
        print("5. Clients with Addresses in City C1 and Driver in City C2")
        print("6. Logout")
        try:
            choice = int(input("Choice (1-6): "))
            clear_terminal()
            match choice:
                case 1: list_cars()
                case 2: manage_drivers()
                case 3: top_client_report()
                case 4: generate_driver_report()
                case 5: find_clients_by_city()
                case 6: break
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Invalid menu choice.")
    
def list_cars():
    sql_query = """
        SELECT Model.modelId, Model.carId, Model.color, Car.brand,
        Model.constructionYear, Model.transmission, COUNT(Rent.rentId) AS times_rented
        FROM Model
        LEFT JOIN Rent ON Model.modelId = Rent.modelId AND Model.carId = Rent.carId
        JOIN Car ON Model.carid = Car.carid
        GROUP BY Model.modelId, Model.carId, Model.color, Model.constructionYear, 
            Model.transmission, Car.brand
        ORDER BY times_rented DESC;
    """
    
    while True:
        car_list = execute_query(sql_query)
        print(f"{'(Car ID, Model ID)':<20} {'Name':<25} {'Times Rented':<13}")
        print("-" * 60)
        for car in car_list:
            car_id_model = f"({car[1]}, {car[0]})"
            car_name = f"{car[2]} {car[3]} {car[4]}"
            print(f"{car_id_model:<20} {car_name:<25} {car[6]:<13}")
        print("-" * 60)

        print("CAR MANAGEMENT")
        print("1. Add Car")
        print("2. Remove Car")
        print("3. Back")
        try:
            choice = int(input("Choice (1-3): "))
            clear_terminal()
            match choice:
                case 1: add_car(car_list)
                case 2: remove_car(car_list)
                case 3: break
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Invalid menu choice.")

def add_car(car_list):
    print(f"{'(Car ID, Model ID)':<20} {'Name':<25} {'Times Rented':<13}")
    print("-" * 60)
    for car in car_list:
        car_id_model = f"({car[1]}, {car[0]})"
        car_name = f"{car[2]} {car[3]} {car[4]}"
        print(f"{car_id_model:<20} {car_name:<25} {car[6]:<13}")
    print("-" * 60)

    try:
        carID = int(input("Enter Car ID: "))
        modelID = int(input("Enter Model ID: "))
    except ValueError:
        clear_terminal()
        print("Invalid Car/Model ID... returning to Car Management menu.")
        return
    
    sql_check_carid = f"""
        SELECT * FROM car WHERE carid = {carID}
    """
    
    sql_check_carmodel = f"""
        SELECT * FROM model WHERE carid = {carID} AND modelid = {modelID}
    """

    # check car id
    res_carid = execute_query(sql_check_carid)
    if len(res_carid) == 0:
        print('Car Brand doesn\'t exist!')
        carBrand = input("Enter Car Brand: ")
        insert_car = f"""
            INSERT INTO Car (carid, brand) VALUES
            ({carID}, '{carBrand}')
        """
        update_table(insert_car)
    else:
        print("Car Brand exists!")
        print(f"Car Brand chosen: {res_carid[0][1]}")

    # check model id
    res_carmodel = execute_query(sql_check_carmodel)
    if len(res_carmodel) != 0:
        clear_terminal()
        print("Car Model exists! Returning to car management...")
        return

    print("Car Model doesn\'t exist! Enter details...")
    try:
        constructionYear = int(input("Enter car\'s construction year: "))
    except ValueError:
        clear_terminal()
        print("Invalid Construction Year... returning to Car Management menu.")
        return
    
    transmission = input("Enter car\'s transmission: ")
    color = input("Enter car\'s color: ")

    insert_model = f"""
        INSERT INTO model (color, constructionYear, transmission, modelId, carid) VALUES
        ('{color}', {constructionYear}, '{transmission}', {modelID}, {carID})
    """
    update_table(insert_model)

def remove_car(car_list):
    print(f"{'(Car ID, Model ID)':<20} {'Name':<25} {'Times Rented':<13}")
    print("-" * 60)
    for car in car_list:
        car_id_model = f"({car[1]}, {car[0]})"
        car_name = f"{car[2]} {car[3]} {car[4]}"
        print(f"{car_id_model:<20} {car_name:<25} {car[6]:<13}")
    print("-" * 60)

    try:
        carID = int(input("Enter Car ID to remove from: "))
        modelID = int(input("Enter Model ID to remove (or 0 to skip model removal): "))
    except ValueError:
        clear_terminal()
        print("Invalid Car/Model ID... returning to Car Management menu.")
        return
    
    if modelID != 0:
        # Removing a specific model first
        confirm_model = input(f"Are you sure you want to remove Model {modelID} from Car {carID}? (y/n): ").lower()
        if confirm_model == 'y':
            delete_rent_model = f"""
                DELETE FROM Rent WHERE modelId = {modelID} AND carId = {carID};
            """
            delete_drives_model = f"""
                DELETE FROM drives WHERE modelId = {modelID} AND carId = {carID};
            """
            delete_model = f"""
                DELETE FROM Model WHERE modelId = {modelID} AND carId = {carID};
            """
            update_table(delete_rent_model)
            update_table(delete_drives_model)
            update_table(delete_model)

            clear_terminal()
            print(f"Model {modelID} removed from Car {carID}.")
        else:
            clear_terminal()
            print("Model removal canceled.")

    # After model deletion (or no model deletion), ask about full car removal
    confirm_car = input(f"Do you also want to completely remove Car {carID}? (y/n): ").lower()
    if confirm_car == 'y':
        delete_rent_car = f"""
            DELETE FROM Rent WHERE carId = {carID};
        """
        delete_drives_car = f"""
            DELETE FROM drives WHERE carId = {carID};
        """
        delete_model_car = f"""
            DELETE FROM Model WHERE carId = {carID};
        """
        delete_car = f"""
            DELETE FROM Car WHERE carId = {carID};
        """
        update_table(delete_rent_car)
        update_table(delete_drives_car)
        update_table(delete_model_car)
        update_table(delete_car)

        clear_terminal()
        print(f"Car {carID} and all its models removed.")
    else:
        clear_terminal()
        print("Car removal canceled. Any deleted models remain deleted.")

def manage_drivers():
    sql_query = """SELECT * FROM driver"""
    
    while True:
        driver_list = execute_query(sql_query)
        print(f"{'Name':<20} {'Address':<25}")
        print("-" * 50)
        for driver in driver_list:
            driver_name = driver[0]
            driver_address = f"{driver[1]} {driver[2]} {driver[3]}"
            print(f"{driver_name:<20} {driver_address:<25}")
        print("-" * 50)

        print("DRIVER MANAGEMENT")
        print("1. Add Driver")
        print("2. Remove Driver")
        print("3. Back")
        try:
            choice = int(input("Choice (1-3): "))
            clear_terminal()
            match choice:
                case 1: add_driver(driver_list)
                case 2: remove_driver(driver_list)
                case 3: break
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Invalid menu choice.")

def add_driver(driver_list):
    print(f"{'Name':<20} {'Address':<25}")
    print("-" * 50)
    for driver in driver_list:
        driver_name = driver[0]
        driver_address = f"{driver[1]} {driver[2]} {driver[3]}"
        print(f"{driver_name:<20} {driver_address:<25}")
    print("-" * 50)
    
    driver_name = input("Enter driver's name: ").strip()
    road_name = input("Enter driver's road name: ").strip()
    try:
        address_number = int(input("Enter driver's address number: "))
    except ValueError:
        clear_terminal()
        print("Invalid address number... returning to Driver Management menu.")
        return
    city = input("Enter driver's city: ").strip()

    # Check if address already exists
    sql_check_address = f"""
        SELECT * FROM Address
        WHERE roadName = '{road_name}' AND addressNumber = {address_number} AND city = '{city}'
    """
    res_address = execute_query(sql_check_address)
    if len(res_address) == 0:
        # Insert address if not exists
        insert_address = f"""
            INSERT INTO Address (roadName, addressNumber, city) VALUES
            ('{road_name}', {address_number}, '{city}')
        """
        update_table(insert_address)
        print("Address added.")

    # Insert driver
    insert_driver = f"""
        INSERT INTO Driver (name, addressNumber, roadName, city) VALUES
        ('{driver_name}', {address_number}, '{road_name}', '{city}')
    """
    update_table(insert_driver)
    print(f"Driver {driver_name} added successfully.")

def remove_driver(driver_list):
    print(f"{'Name':<20} {'Address':<25}")
    print("-" * 50)
    for driver in driver_list:
        driver_name = driver[0]
        driver_address = f"{driver[1]} {driver[2]} {driver[3]}"
        print(f"{driver_name:<20} {driver_address:<25}")
    print("-" * 50)

    driver_name = input("Enter the driver's name to remove: ").strip()

    confirm = input(f"Are you sure you want to remove driver '{driver_name}' and all associated records? (y/n): ").lower()
    if confirm != 'y':
        print("Driver removal canceled.")
        return

    # Deleting associated records
    delete_rent = f"""
        DELETE FROM Rent WHERE name = '{driver_name}';
    """
    delete_review = f"""
        DELETE FROM Review WHERE name = '{driver_name}';
    """
    delete_drives = f"""
        DELETE FROM drives WHERE name = '{driver_name}';
    """
    delete_driver = f"""
        DELETE FROM Driver WHERE name = '{driver_name}';
    """

    update_table(delete_rent)
    update_table(delete_review)
    update_table(delete_drives)
    update_table(delete_driver)

    clear_terminal()
    print(f"Driver '{driver_name}' and all related data removed successfully.")

def top_client_report():
    try:
        k = int(input("Enter the number of top clients to display (k): "))
        if k <= 0:
            raise ValueError
    except ValueError:
        clear_terminal()
        print("Invalid number. Returning to menu...")
        return

    sql_top_clients = f"""
        SELECT Client.name, Client.email, COALESCE(COUNT(Rent.rentID), 0) AS total_rents
        FROM Client
        LEFT JOIN Rent ON Client.email = Rent.email
        GROUP BY Client.name, Client.email
        ORDER BY total_rents DESC
        LIMIT {k}
    """

    top_clients = execute_query(sql_top_clients)

    if not top_clients:
        print("No clients found.")
        return

    print(f"\n{'Name':<25} {'Email':<30} {'Total Rents':<12}")
    print("-" * 70)
    for client in top_clients:
        name, email, total_rents = client
        print(f"{name:<25} {email:<30} {total_rents:<12}")
    input("\nPress Enter to continue...")
    clear_terminal()

def generate_driver_report():
    # Define the SQL query
    sql_query = """
        WITH count_rents AS (
            SELECT d.name, COUNT(r.rentid) AS total_rents
            FROM Driver d
            LEFT JOIN Rent r ON d.name = r.name
            GROUP BY d.name
        ),
        avg_ratings AS (
            SELECT d.name, ROUND(AVG(rv.rating), 2) AS average_rating
            FROM Driver d
            LEFT JOIN Review rv ON d.name = rv.name 
            GROUP BY d.name
        )
        
        SELECT cr.name, cr.total_rents, COALESCE(ar.average_rating, 0) AS average_rating
        FROM count_rents cr
        LEFT JOIN avg_ratings ar ON cr.name = ar.name
        ORDER BY cr.total_rents DESC;
    """
    
    # Execute the query
    driver_report = execute_query(sql_query)

    # If there are no results
    if not driver_report:
        print("No drivers found.")
        input("\nPress Enter to continue...")
        return

    # Print the report
    print(f"\n{'Driver Name':<20} {'Total Rents':<12} {'Average Rating':<15}")
    print("-" * 55)
    
    for driver in driver_report:
        driver_name, total_rents, average_rating = driver
        print(f"{driver_name:<20} {total_rents:<12} {average_rating:<15}")

    # Pause for user to read the report
    input("\nPress Enter to continue...")
    clear_terminal()

def find_clients_by_city():
    city1 = input("Enter first city (client's city): ").strip()
    city2 = input("Enter second city (driver's city): ").strip()
    
    sql_query = f"""
        SELECT DISTINCT c.name, c.email
        FROM Client c
        JOIN staysAt s ON c.email = s.email
        JOIN Address a1 ON s.roadName = a1.roadName AND s.addressNumber = a1.addressNumber AND s.city = a1.city
        JOIN Rent r ON c.email = r.email
        JOIN Driver d ON r.name = d.name
        JOIN Address a2 ON d.roadName = a2.roadName AND d.addressNumber = a2.addressNumber AND d.city = a2.city
        WHERE LOWER(a1.city) = LOWER('{city1}') AND LOWER(a2.city) = LOWER('{city2}');
    """
    results = execute_query(sql_query)
    
    if not results:
        print("\nNo clients found matching those cities.")
    else:
        print(f"\n{'Client Name':<20} {'Email':<30}")
        print("-" * 50)
        for name, email in results:
            print(f"{name:<20} {email:<30}")
    
    input("\nPress Enter to continue...")
    clear_terminal()