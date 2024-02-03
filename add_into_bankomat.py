import sqlite3

def add_values_to_bankomat(values):
    connection = sqlite3.connect("bankomaty.db")
    cursor = connection.cursor()

    for value in values:
        cursor.execute("INSERT INTO Bankomat (Nr_bankomatu, Pieniadze_w_bankomacie) VALUES (?, ?)", value)

    connection.commit()
    connection.close()

if __name__ == "__main__":
    values_to_add = [
        (1, 10000.0),
        (2, 15000.0),
        (3, 20000.0)
    ]

    add_values_to_bankomat(values_to_add)
    print("Values added to Bankomat table.")