import subprocess

# Custom commands to enter:
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel
# sudo python3 -m pip install --force-reinstall adafruit-blinka

# Install required packages
# ##########################
# sudo pip install paho-mqtt
subprocess.run(["sudo", "pip", "install", "paho-mqtt"])
# sudo pip install RPi.GPIO
subprocess.run(["sudo", "pip", "install", "RPi.GPIO"])
# pip install mfrc522
subprocess.run(["sudo", "pip", "install", "mfrc522"])

# Start the mosquitto service
subprocess.run(["sudo", "systemctl", "start", "mosquitto.service"])