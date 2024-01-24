import subprocess

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