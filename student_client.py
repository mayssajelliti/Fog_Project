import requests
import sys

FOG_URL = "http://192.168.1.136:5000/report"

def send_event(event_type):
    if event_type == "scan":
        data = {"src_ip": "192.168.1.130", "unique_ports": 35, "duration": 0.8}
        print(" Envoi d'un événement ANORMAL (scan de ports)...")
    else:
        data = {"src_ip": "192.168.1.130", "unique_ports": 3, "duration": 1.2}
        print(" Envoi d'un événement NORMAL...")
    
    try:
        resp = requests.post(FOG_URL, json=data, timeout=3)
        if resp.json().get("alert"):
            print("  ALERTE déclenchée par le nœud fog !")
        else:
            print(" Comportement jugé NORMAL.")
    except Exception as e:
        print(f" Erreur : {e}")

if __name__ == "__main__":
    event = sys.argv[1] if len(sys.argv) > 1 else "normal"
    send_event("scan" if event == "scan" else "normal")

