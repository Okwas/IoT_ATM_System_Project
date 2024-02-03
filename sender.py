#!/usr/bin/env python3

from tkinter import messagebox
import paho.mqtt.client as mqtt
import tkinter
from bankomat import *

# The terminal ID - can be any string.
terminal_id = "2"
# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()

def call_action(action,argument):
    client.publish("worker/name", action + ","+ str(argument) +"," + terminal_id,)

def call_worker(action):
    client.publish("worker/name", action +"," + terminal_id,)



def create_main_window():
    window.geometry("400x200")
    window.title("SENDER")

    intro_label = tkinter.Label(window, text="Bankomat")
    intro_label.grid(row=0, column=0, columnspan=2)


    entry1 = create_entry(window)
    button1 = tkinter.Button(window, text="Login", command=lambda: call_action("login",get_int(entry1)))
    button1.grid(row=1, column=1, sticky="e")
    button11 = tkinter.Button(window, text="Bad PIN", command=lambda: call_action("input_pin","False"))
    button11.grid(row=1, column=2, sticky="e")

    button2 = tkinter.Button(window, text="Check Balance", command=lambda:call_action("check_balance",""))
    button2.grid(row=2, column=1, sticky="e")

    entry3 = create_entry(window)
    button3 = tkinter.Button(window, text="Deposit", command=lambda: call_action("deposit",get_float(entry3)))
    button3.grid(row=3, column=1, sticky="e")

    entry4 = create_entry(window)
    button4 = tkinter.Button(window, text="Withdraw", command=lambda: call_action("withdraw",get_float(entry4)))
    button4.grid(row=4, column=1, sticky="e")

    button5 = tkinter.Button(window, text="Logout", command=lambda: call_action("logout",""))
    button5.grid(row=5, column=1, sticky="e")

    button_stop = tkinter.Button(window, text="Stop", command=window.quit)
    button_stop.grid(row=7, columnspan=2)

def create_entry(parent):
    entry = tkinter.Entry(parent)
    entry.grid(sticky="w")
    return entry

def get_int(entry):
    try:
        return int(entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid int.")
        return 0

def get_float(entry):
    try:
        return float(entry.get())
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid float.")
        return 0
    

def process_message(client, userdata, message):
    # Decode message.
    message_decoded = (str(message.payload.decode("utf-8"))).split(",")
    message = message_decoded[0]
    id = message_decoded[1]
    if(id==terminal_id):
        print(message_decoded)
    



def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    client.on_message = process_message
    client.loop_start()
    client.subscribe("serwer/name")
    # Send message about conenction.
    call_worker("Client connected")


def disconnect_from_broker():
    # Send message about disconenction.
    call_worker("Client disconnected")
    # Disconnet the client.
    client.disconnect()


def run_sender():
    connect_to_broker()
    create_main_window()

    # Start to display window (It will stay here until window is displayed)
    window.mainloop()

    disconnect_from_broker()


if __name__ == "__main__":
    run_sender()
