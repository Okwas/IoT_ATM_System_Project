import sqlite3
import time
import os


def create_database():
    if os.path.exists("bankomaty.db"):
        os.remove("bankomaty.db")
        print("Stara baza usunięta")
    connection = sqlite3.connect("bankomaty.db")
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Bankomat (
            Nr_bankomatu INTEGER PRIMARY KEY,
            Pieniadze_w_bankomacie REAL
        )
    ''')

    # Create Client table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Konto (
            Nr_konta TEXT PRIMARY KEY,
            Pieniadze_na_koncie REAL
        )
    ''')
    connection.commit()
    connection.close()
    print("Nowa baza stworzona")




if __name__ == "__main__":
    create_database()