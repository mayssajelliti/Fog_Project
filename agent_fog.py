# agent_windows.py
import subprocess
import time
import requests

FOG_URL = "http://127.0.0.1:5000/report"  # Communique avec le nœud fog local

def get_remote_ports():
    """ Récupère le nombre de ports distants uniques via PowerShell """
    try:
        result = subprocess.run([
            "powershell", "-Command",
            "Get-NetTCPConnection | Where-Object {$_.State -eq 'Established'} | ForEach-Object {$_.RemotePort}"
        ], capture_output=True, text=True, timeout=5)
        
        ports = set()
        for line in result.stdout.strip().split("\n"):
            if line.strip().isdigit():
                ports.add(int(line.strip()))
        return len(ports)
    except Exception as e:
        return 0

def main():
    print("📡 Agent Windows en surveillance (Ctrl+C pour arrêter)")
    while True:
        start_time = time.time()
        port_counts = []

        # Surveille pendant 15 secondes
        for _ in range(15):
            count = get_remote_ports()
            port_counts.append(count)
            time.sleep(1)

        unique_ports = max(port_counts) if port_counts else 0
        duration = time.time() - start_time

        # Envoie les métriques au nœud fog
        payload = {
            "src_ip": "127.0.0.1",
            "unique_ports": unique_ports,
            "duration": duration
        }

        try:
            response = requests.post(FOG_URL, json=payload, timeout=3)
            if response.json().get("alert"):
                print(" ALERTE : Comportement anormal détecté !")
            else:
                print(f" {unique_ports} ports contactés en {duration:.1f}s")
        except Exception as e:
            print("Nœud Fog injoignable")

        time.sleep(5)  # Pause avant le prochain cycle

if __name__ == "__main__":
    main()