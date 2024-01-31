import sqlite3


session_client = {
    "t0": "",
    "t1": "",
    "t2": ""
}
session_flag = {
    "t0": False,
    "t1": False,
    "t2": False
}
# potrzebna bedzie zmienna z aktualnym bankomatem


# Sprawdzenie, czy konto istanieje
def account_exists(RFID):
    connection = sqlite3.connect("bankomaty.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Konto WHERE Nr_konta=?", (RFID,))
    count = cursor.fetchone()[0]

    connection.close()

    return count > 0


# Tworzenie konta
def create_account(RFID):
    connection = sqlite3.connect("bankomaty.db")
    cursor = connection.cursor()
    cursor.execute("INSERT INTO Konto (Nr_konta, Pieniadze_na_koncie) VALUES (?, ?)", (RFID, 5000.0))
    connection.commit()

    connection.close()


# Sprawdzenie czy jest zalogowany użytkownik
def is_logged_in(ATM):
    global session_client
    global session_flag
    return session_client[ATM] != "" and session_flag[ATM]



# Sprawdza, czy któryś bankomat obsługuje już dane konto
def is_card_in_use(RFID):
    for card in session_client.values():
        if card == RFID:
            return True
    return False




# Loguje
def login(RFID,ATM):
    if is_card_in_use(RFID) == False:
        if account_exists(RFID) == False:
            create_account(RFID)
        global session_client
        session_client[ATM] = RFID
        # Tu pętla która sprawdza pin, narazie dam zawsze true
        input_pin(True,ATM)
    else:
        print("Card already in use")


def input_pin(isCorrect,ATM):
    if isCorrect:
        global session_flag
        session_flag[ATM] = True
    else:
        # Buzzer
        return None
    

# Tu chyba nigdy zmian nie bedzie trzeba robic
def check_balance(ATM):
    if is_logged_in(ATM):
            connection = sqlite3.connect("bankomaty.db")
            cursor = connection.cursor()
            cursor.execute("SELECT Pieniadze_na_koncie FROM Konto WHERE Nr_konta=?", (session_client[ATM],))
            balance = cursor.fetchone()[0]
            connection.close()
            print(f"Balance for account {session_client[ATM]}: {balance}")
            return balance
        

# Dobrze by było zrobic tak, że liczba pieniedzy w bankomacie się zwieksza
def deposit(amount,ATM):
    if is_logged_in(ATM):
        connection = sqlite3.connect("bankomaty.db")
        cursor = connection.cursor()
        


        cursor.execute("UPDATE Konto SET Pieniadze_na_koncie = Pieniadze_na_koncie + ? WHERE Nr_konta=?", (amount, session_client[ATM]))
        connection.commit()

        connection.close()
        print(f"Deposited {amount} to account {session_client[ATM]}.")




def withdraw(amount,ATM):
    if is_logged_in(ATM):
        connection = sqlite3.connect("bankomaty.db")
        cursor = connection.cursor()

        current_balance = check_balance(ATM)

        #      TU POWINIEN BYĆ CHECK NA PIENIADZE W BANKOMACIE, ALE NIE ROBIE TEGO BO BANKOMAT BEDZIEMY TWORZYC RAZEM Z MQTT CHYBA
        # cursor.execute("SELECT Pieniadze_w_bankomacie FROM Bankomat WHERE Nr_bankomatu=?",())
        # atm_balance = 

        if current_balance >= amount and amount > 0:
            cursor.execute("UPDATE Konto SET Pieniadze_na_koncie = Pieniadze_na_koncie - ? WHERE Nr_konta=?", (amount, session_client[ATM]))
            connection.commit()
            print(f"Withdrew {amount} from account {session_client[ATM]}.")
        else:
            print("Invalid withdrawal amount or insufficient funds.")

        connection.close()


# Tu trzeba bedzie nasłuchiwanie dodać
def logout(ATM):
    if is_logged_in(ATM):
        global session_client
        global session_flag
        session_client[ATM] = ""
        session_flag[ATM] = False



# Tu sobie wpisujesz komendy, np login(123), input_pin(True), check_balance()
if __name__ == "__main__":
    print("Welcome to the interactive bank script!")
    print("Available functions: create_account, is_logged_in, login, input_pin, check_balance, withdraw, deposit, logout")
    print("To exit, type 'exit'.")

    while True:
        user_input = input(">>> ")

        if user_input.lower() == 'exit':
            print("Exiting...")
            break
        
        try:
            eval_result = eval(user_input)
        except Exception as e:
            print(f"Error: {e}")