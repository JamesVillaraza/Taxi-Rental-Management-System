def check_exisiting_mngrssn(ssn, cursor):
    script = """
        SELECT ssn FROM manager
    """
    cursor.execute(script)
    record = cursor.fetchall()
    record = [x[0] for x in record]
    if ssn in record: return True
    else: return False

def check_exisiting_email(email, cursor):
    script = """
        SELECT email FROM client
    """
    cursor.execute(script)
    record = cursor.fetchall()
    record = [x[0] for x in record]
    if email in record: return True
    else: return False

def check_existing_address(address, cursor):
    script = "SELECT * FROM address"
    cursor.execute(script)
    record = [(x[0], x[1], x[2]) for x in cursor.fetchall()]  # (roadname, addressnumber, city)

    for existing in record:
        if ( # case-insensitive comparison
            address[0].lower() == existing[0].lower() and
            address[1] == existing[1] and
            address[2].lower() == existing[2].lower()
        ):
            return True, existing  # Match found; return True and formatted tuple

    return False, address  # No match; return original

def check_existing_card(cardNum, cursor):
    script = "SELECT creditcardnumber FROM creditcard"
    cursor.execute(script)
    record = [x[0] for x in cursor.fetchall()]
    if cardNum in record: return True
    else: return False