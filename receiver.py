#!/usr/bin/env python3

import paho.mqtt.client as mqtt
import tkinter
import sqlite3
import time
from bankomat import *

# The broker name or IP address.
# broker = "localhost"
broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()

# Thw main window.
window = tkinter.Tk()

def return_to_client(action,terminal_id):
    client.publish("serwer/name", action+","+str(terminal_id))

def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")
    print(message_decoded)
    action = message_decoded[0]
    argument = message_decoded[1]
    if len(message_decoded)>2:
        atm = message_decoded[2]
        if action == "login":
            
            return_to_client(login(argument,atm),atm)
        elif action == "check_balance":
            
            return_to_client(str(check_balance(atm)),atm)
        elif action == "deposit":
            
            return_to_client(deposit(float(argument),atm),atm)
        elif action == "withdraw":
            
            return_to_client(withdraw(float(argument),atm),atm)
        elif action == "input_pin":
            
            return_to_client(input_pin(bool(argument),atm),atm)
        else:
            logout(atm)

def print_log_to_window():
    connention = sqlite3.connect("workers.db")
    cursor = connention.cursor()
    cursor.execute("SELECT * FROM workers_log")
    log_entries = cursor.fetchall()
    labels_log_entry = []
    print_log_window = tkinter.Tk()

    for log_entry in log_entries:
        labels_log_entry.append(tkinter.Label(print_log_window, text=(
            "On %s, %s used the terminal %s" % (log_entry[0], log_entry[1], log_entry[2]))))

    for label in labels_log_entry:
        label.pack(side="top")

    connention.commit()
    connention.close()

    # Display this window.
    print_log_window.mainloop()

def create_main_window():
    window.geometry("250x100")
    window.title("RECEIVER")
    label = tkinter.Label(window, text="Listening to the MQTT")
    exit_button = tkinter.Button(window, text="Stop", command=window.quit)
    print_log_button = tkinter.Button(
        window, text="Print log", command=print_log_to_window)

    label.pack()
    exit_button.pack(side="right")
    print_log_button.pack(side="right")

def connect_to_broker():
    client.connect(broker)
    # Send message about conenction.
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("worker/name")
    client.subscribe("login")

def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()

def run_receiver():
    connect_to_broker()
    create_main_window()
    # Start to display window (It will stay here until window is displayed)
    window.mainloop()
    disconnect_from_broker()


if __name__ == "__main__":
    run_receiver()
