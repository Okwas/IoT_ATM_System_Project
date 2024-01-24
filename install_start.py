import subprocess

# Install required packages
subprocess.run(["sudo", "pip", "install", "paho-mqtt"])

# Start the mosquitto service
subprocess.run(["sudo", "systemctl", "start", "mosquitto.service"])