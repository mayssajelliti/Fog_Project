# agent_windows.py
import subprocess
import time
import requests

FOG_URL = "http://127.0.0.1:5001/report"

def get_remote_ports():
    try:
        result = subprocess.run([
            "powershell", "-Command",
            "Get-NetTCPConnection | Where-Object {$_.State -eq 'Established'} | ForEach-Object {$_.RemotePort}"
        ], capture_output=True, text=True, timeout=5)
        ports = {int(p.strip()) for p in result.stdout.split() if p.strip().isdigit()}
        return len(ports)
    except:
        return 0

def main():
    print(" Agent Windows en surveillance (Ctrl+C pour arrêter)")
    while True:
        start = time.time()
        counts = [get_remote_ports() for _ in range(15)]
        unique_ports = max(counts)
        duration = time.time() - start

        payload = {"src_ip": "127.0.0.1", "unique_ports": unique_ports, "duration": duration}
        try:
            resp = requests.post(FOG_URL, json=payload, timeout=3)
            if resp.json().get("alert"):
                print(" ALERTE : Comportement anormal détecté !")
            else:
                print(f" {unique_ports} ports contactés")
        except:
            print(" Fog injoignable")
        time.sleep(10)

if __name__ == "__main__":
    main()