#!/usr/bin/env python3
import datetime, neopixel, board
import uuid, time

import paho.mqtt.client as mqtt
import tkinter

import RPi.GPIO as GPIO

from config import *
from mfrc522 import MFRC522

from PIL import Image, ImageDraw, ImageFont
import lib.oled.SSD1331 as SSD1331

BOUNCE_TIME = 100

# The terminal ID - can be any string.
terminal_id = "T0"
# The broker name or IP address.
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"

# The MQTT client.
client = mqtt.Client()

# Thw main window with buttons to simulate the RFID card usage.
window = tkinter.Tk()

# variables global
session_flag = False

class Color:
    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    light_green = (0, 128, 0)
    yellow = (255, 255, 0)

pixels = neopixel.NeoPixel(board.D18, 8, brightness=1.0 / 32, auto_write=False)

def clear():
    pixels.show()
    pixels.fill((0, 0, 0))
    pixels.show()
    
def successful_reading():
    pixels.show()
    pixels.fill(Color.light_green)
    pixels.show()

def successful_reading_temp():
    pixels.show()
    pixels.fill(Color.light_green)
    pixels.show()
    time.sleep(3)
    pixels.fill((0, 0, 0))
    pixels.show()

def failed_reading():
    pixels.show()
    pixels.fill(Color.red)
    pixels.show()

def failed_reading_temp():
    pixels.show()
    pixels.fill(Color.red)
    pixels.show()
    time.sleep(3)
    pixels.fill((0, 0, 0))
    pixels.show()

def wait_reading():
    pixels.show()
    pixels.fill(Color.yellow)
    pixels.show()

class RFIDHandler:
    def __init__(self):
        self.MIFAREReader = MFRC522()
        self.was_read: bool = False
        self.last_detection: datetime = None
        self.last_card_uid = None
        self.log_id = 0
        self.machine_id = 1

    def read(self):
        (status, TagType) = self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        if status == self.MIFAREReader.MI_OK:
            (status, uid) = self.MIFAREReader.MFRC522_Anticoll()
            if status == self.MIFAREReader.MI_OK:
                new_time = datetime.datetime.now()
                if not self.was_read:
                    self.was_read = True
                    self.last_detection = new_time
                    self.last_card_uid = uid
                    self.log_id += 1
                    return self.was_read
                return self.was_read
        else:
            self.was_read = False
        return self.was_read

    def get_data(self):
        data = {
            "log_id": str(self.log_id),
            "date": self.last_detection.strftime("%d-%m-%Y %H:%M:%S"),
            "card_uid": str(self.last_card_uid),
            "reader": (self.machine_id)
        }
        return data


def play_sound_success():
    GPIO.output(buzzerPin, False)
    time.sleep(0.3)
    GPIO.output(buzzerPin, True)


def play_sound_failure():
    for i in range(3):
        GPIO.output(buzzerPin, False)
        time.sleep(0.1)
        GPIO.output(buzzerPin, True)
        time.sleep(0.1)
    GPIO.output(buzzerPin, GPIO.LOW)

execute = True
is_waiting_for_response = False

# OLED
background = Image.new("RGB", (96, 64), "BLACK")
draw = ImageDraw.Draw(background)
font = ImageFont.truetype('./lib/oled/Font.ttf', 10)
disp = SSD1331.SSD1331()

def oled_show():
    disp.ShowImage(background, 0, 0)

def show_input_card_message():
    erase_oled()
    draw.text((25, 10), 'Input', font=font, fill="WHITE")
    draw.text((30, 25), 'Card', font=font, fill="WHITE")
    oled_show()

def show_input_pin_message():
    erase_oled()
    draw.text((25, 10), 'Input', font=font, fill="WHITE")
    draw.text((30, 25), 'PIN', font=font, fill="WHITE")
    oled_show()

def erase_oled():
    draw.rectangle(((0, 0), (96, 64)), fill="BLACK")
    
#uzycie przycisku, wylaczenie programu
def redButtonPressedCallback(channel):
    global execute
    execute = False

# broker
client = mqtt.Client()
broker = "localhost"
# broker = "127.0.0.1"
# broker = "10.0.0.1"


def connect_to_broker():
    # Connect to the broker.
    client.connect(broker)
    print("Client connected")
    client.on_message = process_message
    # Starts client and subscribe.
    client.loop_start()
    client.subscribe("card/response")


def disconnect_from_broker():
    # Disconnet the client.
    client.loop_stop()
    client.disconnect()
    print("Client disconnected")

def publish_card_log(log_id, date, card_uid, reader):
    client.publish("card/info", f'{log_id}#{date}#{card_uid}#{reader}')
    print('Published card read info')

def process_message(client, userdata, message):
    response = (str(message.payload.decode("utf-8")))
    print(f'response: {response}')
    if response == 'HTTP200':
        successful_reading()
        play_sound_success()
    else:
        failed_reading()
        play_sound_failure()
    time.sleep(1)
    show_input_card_message()
    clear()
    global is_waiting_for_response
    is_waiting_for_response = False

def buttonRedPressedCallback(channel):
    # TODO: obsługiwać niepoprawny login (trzeba dopisac backend funkcje login)
    print("\nButton Red connected to GPIO " + str(channel) + " pressed.")
    print("\nPodano NIEpoprawny PIN :<")
    successful_reading_temp()
    play_sound_success()

def buttonGreenPressedCallback(channel):
    # TODO: obsługiwać poprawny login (trzeba dopisac backend funkcje login)
    print("\nButton Green connected to GPIO " + str(channel) + " pressed.")
    print("\nPodano poprawny PIN :>")
    failed_reading_temp()
    play_sound_failure()

def readButtonRedPinInput():
    GPIO.add_event_detect(buttonRed, GPIO.FALLING, callback=buttonRedPressedCallback, bouncetime=200)

def readButtonGreenPinInput():
    GPIO.add_event_detect(buttonGreen, GPIO.FALLING, callback=buttonGreenPressedCallback, bouncetime=200)

# main logic of ATM here
def readCardInLoop():
    global is_waiting_for_response
    rfid_handler = RFIDHandler()
    while execute:
        while not is_waiting_for_response:
            readCardValue = rfid_handler.read()
            if readCardValue:
                erase_oled()
                oled_show()
                is_waiting_for_response = True
                successful_reading_temp()
                log_id, date, card_uid, reader = rfid_handler.get_data().values()
                publish_card_log(log_id, date, card_uid, reader)
                time.sleep(1)
                wait_reading()
                show_input_pin_message()
                readButtonRedPinInput()
                readButtonGreenPinInput()

def main():
    disp.Init()
    disp.clear()
    clear()
    show_input_card_message()
    connect_to_broker()
    readCardInLoop()
    disconnect_from_broker()
    GPIO.cleanup()

if __name__ == "__main__":
    main()
