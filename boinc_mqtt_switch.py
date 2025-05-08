import json
import time
import subprocess
import os
import sys
import paho.mqtt.client as mqtt


def get_project_urls():
    try:
        output = subprocess.check_output(["boinccmd.exe", "--get_project_status"], text=True)
        projects = []
        for line in output.splitlines():
            if line.strip().startswith("master URL:"):
                url = line.strip().split(":", 1)[1].strip()
                projects.append(url)
        return projects
    except Exception as e:
        print("Fehler beim Auslesen der Projekte:", e)
        return []

def suspend_all_projects():
    for url in get_project_urls():
        print("Pausiere:", url)
        subprocess.call(["boinccmd.exe", "--project", url, "suspend"])

def resume_all_projects():
    for url in get_project_urls():
        print("Fortsetzen:", url)
        subprocess.call(["boinccmd.exe", "--project", url, "resume"])

def resource_path(rel_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(os.path.abspath("."), rel_path)

# Lade Konfiguration
CONFIG_FILE = resource_path("config.json")
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

MQTT_BROKER = config["mqtt_host"]
MQTT_PORT = config["mqtt_port"]
MQTT_USERNAME = config["mqtt_username"]
MQTT_PASSWORD = config["mqtt_password"]
DEVICE_ID = config["device_id"]
SWITCH_NAME = config["switch_name"]

STATE_TOPIC = f"homeassistant/switch/{DEVICE_ID}/state"
COMMAND_TOPIC = f"homeassistant/switch/{DEVICE_ID}/set"
AVAILABILITY_TOPIC = f"homeassistant/switch/{DEVICE_ID}/availability"
DISCOVERY_TOPIC = f"homeassistant/switch/{DEVICE_ID}/config"

client = mqtt.Client(protocol=mqtt.MQTTv5)

def on_connect(client, userdata, flags, reason_code, properties):
    print("MQTT verbunden mit Code:", reason_code)
    client.subscribe(COMMAND_TOPIC)

    payload = {
        "name": SWITCH_NAME,
        "unique_id": DEVICE_ID,
        "state_topic": STATE_TOPIC,
        "command_topic": COMMAND_TOPIC,
        "availability_topic": AVAILABILITY_TOPIC,
        "payload_on": "ON",
        "payload_off": "OFF",
        "device": {
            "identifiers": [DEVICE_ID],
            "name": "Windows PC",
            "manufacturer": "Microsoft",
            "model": "BOINC Client"
        }
    }
    client.publish(DISCOVERY_TOPIC, json.dumps(payload), retain=True)
    client.publish(AVAILABILITY_TOPIC, "online", retain=True)
    send_boinc_state()

def on_message(client, userdata, msg):
 if msg.topic == COMMAND_TOPIC:
        command = msg.payload.decode()
        try:
            if command == "ON":
                print("resume calculation")
                resume_all_projects()
            elif command == "OFF":
                print("pausing calculation")
                suspend_all_projects()
            time.sleep(1)
            send_boinc_state()
        except Exception as e:
            print("Fehler beim Ausführen:", e)

def send_boinc_state():
    try:
        output = subprocess.check_output(["boinccmd", "--get_simple_gui_info"], text=True)
        state = "ON" if "suspended via GUI: yes" not in output else "OFF"
    except Exception:
        state = "OFF"
    client.publish(STATE_TOPIC, state, retain=True)

client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
client.on_connect = on_connect
client.on_message = on_message
client.will_set(AVAILABILITY_TOPIC, "offline", retain=True)
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

try:
    while True:
        send_boinc_state()
        time.sleep(60)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
