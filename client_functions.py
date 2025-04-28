from utility import clear_terminal, update_table, execute_query
from datetime import datetime

def client_login():
    sql_query = """SELECT email FROM client"""
    client_emails = [x[0] for x in execute_query(sql_query)]
    print(client_emails)

    print("CLIENT LOGIN")
    print("------------")
    client_email = input("Enter Email to login (case-sensitive): ")

    clear_terminal()

    if client_email not in client_emails:
        print("Invalid Email Login... returning to login menu.")
        return

    # at this point we are logged in
    client_menu(client_email)

def client_menu(client_email):
    while(True):
        print(f"CLIENT MENU -- {client_email}")
        print('---------------' + ('-' * len(client_email)))
        print("1. List Available Car Models")
        print("2. Book & Rent Driver")
        print("3. Your Booking History")
        print("4. Write Review")
        print("5. Logout")
        try:
            choice = int(input("Choice (1-5): "))
            clear_terminal()
            match choice:
                case 1: list_available_cars()
                case 2: book_driver(client_email)
                case 3: booking_history(client_email)
                case 4: write_review(client_email)
                case 5: break
                case _: raise ValueError
        except ValueError:
            clear_terminal()
            print("Invalid menu choice.")

def list_available_cars():
    print("AVAILABLE CARS ON A SPECIFIC DATE")
    print("----------------------------------")

    # ask for date
    date_d = input("Enter the desired date (YYYY-MM-DD): ").strip()

    # validate the date format using datetime
    try:
        datetime.strptime(date_d, "%Y-%m-%d")  # this will raise ValueError if format is wrong
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    # build the query using the user's date
    sql_query = f"""
        WITH available_driver_model_pairs AS (
            SELECT d.name, d.modelId, d.carId
            FROM drives d
            WHERE d.name NOT IN (
                SELECT r.name
                FROM Rent r
                WHERE r.date = '{date_d}'
            )
        )
        SELECT DISTINCT dmp.modelId, dmp.carId
        FROM available_driver_model_pairs dmp
        ORDER BY dmp.modelId, dmp.carId;
    """

    try:
        # execute query
        available_cars = execute_query(sql_query)

        # display results
        if available_cars:
            print(f"\nAvailable car models on {date_d}:")
            print("-" * 30)
            for modelid, carid in available_cars:
                print(f"ModelID: {modelid}, CarID: {carid}")
            input("\nPress Enter to continue...")
            clear_terminal()
        else:
            print(f"No available car models found for {date_d}.")
    except Exception as e:
        print(f"An error occurred while fetching available cars: {e}")

def book_driver(client_email):
    try:
        # ask user for modelId, carId, and date
        carid = int(input("Enter CarID you want to rent: ").strip())
        modelid = int(input("Enter ModelID you want to rent: ").strip())

        # validate if CarID exists
        sql_validate_car = f"SELECT carid FROM car WHERE carid = {carid};"
        car_exists = execute_query(sql_validate_car)
        
        # validate if ModelID exists
        sql_validate_model = f"SELECT modelid FROM model WHERE modelid = {modelid} AND carid = {carid};"
        model_exists = execute_query(sql_validate_model)

        if not car_exists:
            print(f"Error: CarID {carid} does not exist.")
        elif not model_exists:
            print(f"Error: ModelID {modelid} does not exist for CarID {carid}.")

        rent_date = input("Enter rental date (YYYY-MM-DD): ").strip()

        # validate date format
        from datetime import datetime
        try:
            datetime.strptime(rent_date, "%Y-%m-%d")
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
            return

        # find an available driver
        sql_find_driver = f"""
            SELECT d.name
            FROM drives d
            WHERE d.modelId = {modelid}
              AND d.carId = {carid}
              AND d.name NOT IN (
                  SELECT r.name
                  FROM Rent r
                  WHERE r.date = '{rent_date}'
              )
            LIMIT 1;
        """

        result = execute_query(sql_find_driver)

        if not result:
            print(f"No available drivers for CarID {carid}, ModelID {modelid} on {rent_date}.")
            return
        
        # get driver name
        driver_name = result[0][0]

        sql_get_max_rentid = "SELECT COALESCE(MAX(rentId), 0) FROM Rent;"
        result = execute_query(sql_get_max_rentid)
        new_rentid = result[0][0] + 1  # safely handle empty table

        # insert the rent
        sql_insert_rent = f"""
            INSERT INTO Rent (rentID, email, name, modelId, carId, date)
            VALUES ({new_rentid}, '{client_email}', '{driver_name}', {modelid}, {carid}, '{rent_date}');
        """
        try:
            update_table(sql_insert_rent)  # try inserting
            print(f"Successfully booked! Assigned driver: {driver_name}")  # only print if success
        except Exception as e:
            return
        
        input("\nPress Enter to continue...")
        clear_terminal()

    except ValueError:
        print("CarID and ModelID must be numbers.")
    except Exception as e:
        print(f"An error occurred: {e}")
        return

def booking_history(client_email):
    # sql query
    sql_query = f"""
        SELECT
            r.rentId,
            r.date,
            r.name AS driver_name,
            m.modelId,
            m.carId
        FROM Rent r
        JOIN Model m ON r.modelId = m.modelId AND r.carId = m.carId
        WHERE r.email = '{client_email}'
        ORDER BY r.date ASC;
    """

    try:
        history = execute_query(sql_query)

        if history:
            print(f"Booking history for {client_email}:")
            print("-" * 60)
            for rentId, date, driver_name, modelId, carId, in history:
                print(f"Date: {date}    Driver: {driver_name}")
                print(f"Car ID: {carId}    Model ID: {modelId}")
                print("-" * 60)
            input("\nPress Enter to continue...")
            clear_terminal()
        else:
            clear_terminal()
            print(f"No booking history found for {client_email}.")
    except Exception as e:
        clear_terminal()
        print(f"An error occurred while fetching booking history: {e}")

def write_review(client_email):
    print("\nWRITE A REVIEW")
    print("----------------")

    # Ask for driver's name
    driver_name = input("Enter the driver's name (case-sensitive): ").strip()

    # Check if client has rented with the driver
    sql_check_driver = f"""
        SELECT 1
        FROM Rent r
        WHERE r.email = '{client_email}'
          AND r.name = '{driver_name}'
        LIMIT 1;
    """
    result = execute_query(sql_check_driver)

    if not result:
        clear_terminal()
        print(f"You have not rented a car from {driver_name}, so you cannot leave a review.")
        return

    sql_max_review_id = "SELECT MAX(reviewId) FROM Review;"
    max_review_id = execute_query(sql_max_review_id)
        
    # If the table is empty, start the reviewId from 1
    if not max_review_id or max_review_id[0][0] is None:
        new_review_id = 1
    else:
        new_review_id = max_review_id[0][0] + 1

    # Ask for the review details
    try:
        rating = int(input("Enter a rating (1-5): ").strip())
        if rating < 1 or rating > 5:
            print("Rating must be between 1 and 5.")
            return
    except ValueError:
        print("Invalid rating. Please enter a number between 1 and 5.")
        return

    review_message = input("Enter your review message: ").strip()

    # Insert the review into the database
    sql_insert_review = f"""
        INSERT INTO Review (reviewid, name, rating, message, email)
        VALUES ({new_review_id}, '{driver_name}', {rating}, '{review_message}', '{client_email}');
    """

    try:
        update_table(sql_insert_review)
        print(f"Review for {driver_name} has been successfully submitted!")
    except Exception as e:
        print(f"An error occurred while submitting the review: {e}")
    
    input("\nPress Enter to continue...")
    clear_terminal()