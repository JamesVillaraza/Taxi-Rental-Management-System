import psycopg2
import os

# create connection and cursor globally #
connection = psycopg2.connect(database="postgres", user='postgres', password='123', host="localhost", port=5432)
cursor = connection.cursor()

#############################################

# utility functions #
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_table(script): # for inserting or deleting in tables
    try:
        cursor.execute(script)
        connection.commit()
        print("Success!")
    except Exception as e:
        # clear_terminal()
        print("An error occurred: ", e)
        raise e

def execute_query(query): # for retrieving sql queries
    try:
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print("An error occurred: ", e)
        raise e