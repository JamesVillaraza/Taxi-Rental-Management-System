def insert_dummy_data(connection, cursor):
    sql_script = """
    -- Additional Clients
    INSERT INTO Client (name, email) VALUES
    ('Ivy Green', 'ivy@mail.com'),
    ('Jack Hill', 'jack@mail.com');

    -- Additional Addresses
    INSERT INTO Address (roadName, addressNumber, city) VALUES
    ('Cedar Ln', 505, 'Riverdale'),
    ('Birch Blvd', 606, 'Greenville');

    -- Additional staysAt (client addresses)
    INSERT INTO staysAt (roadName, addressNumber, city, email) VALUES
    ('Cedar Ln', 505, 'Riverdale', 'ivy@mail.com'),
    ('Elm St', 303, 'Springfield', 'jack@mail.com');

    -- Additional CreditCards
    INSERT INTO CreditCard (creditCardNumber, email, addressNumber, roadName, city) VALUES
    (456789, 'ivy@mail.com', 505, 'Cedar Ln', 'Riverdale'),
    (567890, 'jack@mail.com', 303, 'Elm St', 'Springfield');

    -- Additional Drivers
    INSERT INTO Driver (name, addressNumber, roadName, city) VALUES
    ('Hank Miles', 505, 'Cedar Ln', 'Riverdale'),
    ('Luna Drive', 606, 'Birch Blvd', 'Greenville');

    -- Additional drives
    INSERT INTO drives (name, modelId, carId) VALUES
    ('Hank Miles', 1, 1),
    ('Luna Drive', 2, 1);

    -- Additional Rents
    INSERT INTO Rent (rentId, date, modelId, carId, name, email) VALUES
    (5, '2025-04-19', 1, 1, 'Hank Miles', 'ivy@mail.com'),
    (6, '2025-04-20', 2, 1, 'Luna Drive', 'jack@mail.com');

    -- Additional Reviews
    INSERT INTO Review (reviewId, name, rating, message, email) VALUES
    (4, 'Hank Miles', 4, 'Very polite and professional', 'ivy@mail.com'),
    (5, 'Luna Drive', 5, 'Perfect drive!', 'jack@mail.com');

    """

    # updating/deleting table instances
    try:
        cursor.execute(sql_script)
        connection.commit()
        print("Dummy Data inserted!!")
    except Exception as e:
        print("An error ocurred: ", e)