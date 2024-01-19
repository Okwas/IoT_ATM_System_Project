import sqlite3

def print_database():
    # Connect to SQLite database
    conn = sqlite3.connect('bankomaty.db')
    cursor = conn.cursor()

    # Print Bankomat table
    print("Bankomat table:")
    cursor.execute("SELECT * FROM Bankomat")
    bankomat_rows = cursor.fetchall()
    print("{:<15} {:<10}".format("Nr_bankomatu", "Pieniadze_w_bankomacie"))
    for row in bankomat_rows:
        print("{:<15} {:<10}".format(row[0], row[1]))

    # Print Client table
    print("\nClient table:")
    cursor.execute("SELECT * FROM Konto")
    client_rows = cursor.fetchall()
    print("{:<20} {:<10}".format("Nr_konta", "Pieniadze_na_koncie"))
    for row in client_rows:
        print("{:<20} {:<10}".format(row[0], row[1]))

    # Close connection
    conn.close()

if __name__ == "__main__":
    print_database()