import socket  
import time
import subprocess
import sys

# --- Constants ---
HOST = "127.0.0.1"
PORT = int(input("Port: "))
LOG_FILE = "command_log.txt"

# --- Connection ---
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", PORT))
server.listen(1)
conn, addr = server.accept()

print(f"[+] Connected to {addr}")

# --- 
while True:
    try:
        command = input("You: ").strip()
        if not command:
            continue
        conn.send(command.encode())
        response = conn.recv(65536).decode()
        if response == "Exit":
            print("Exiting...")
            break
        print(response)
    except Exception as e:
        print(f"[!] Error: {e}")
        time.sleep(5)
        subprocess.run([sys.executable, *sys.argv])

    except KeyboardInterrupt:
        print("\n[-] Closing server...")
        conn.close()
        break