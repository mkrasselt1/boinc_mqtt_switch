# BOINC MQTT Switch

Dieses Projekt ermöglicht die Steuerung eines BOINC-Clients über MQTT. Es integriert sich in Home Assistant und erlaubt das Pausieren und Fortsetzen von Berechnungen über MQTT-Befehle.

## Projektstruktur
boinc_mqtt_switch.py # Hauptskript für die MQTT-Integration 
config.json # Konfigurationsdatei für MQTT und Geräteinformationen 
requirements.txt # Abhängigkeiten des Projekts

## Voraussetzungen

- Python 3.x
- BOINC-Client installiert und `boinccmd` verfügbar
- MQTT-Broker (z. B. Mosquitto)
- Home Assistant (optional, für die Integration)

## Installation

1. Klone dieses Repository oder lade die Dateien herunter.
2. Installiere die Abhängigkeiten:
   ```bash
   pip install -r requirements.txt
   ```
3. Konfiguriere die Datei config.json mit den MQTT- und Geräteinformationen.

## Verwendung
Starte das Skript:
Das Skript verbindet sich mit dem MQTT-Broker und veröffentlicht die Geräteinformationen.
Verwende MQTT-Befehle, um den BOINC-Client zu steuern:
ON: Fortsetzen der Berechnungen
OFF: Pausieren der Berechnungen
MQTT-Topics
State Topic: homeassistant/switch/<device_id>/state
Command Topic: homeassistant/switch/<device_id>/set
Availability Topic: homeassistant/switch/<device_id>/availability
Discovery Topic: homeassistant/switch/<device_id>/config

## Fehlerbehebung
Stelle sicher, dass boinccmd im Systempfad verfügbar ist.
Überprüfe die MQTT-Broker-Verbindung und die Konfiguration in config.json.

## Lizenz
Dieses Projekt steht unter der MIT-Lizenz