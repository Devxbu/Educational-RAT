import socket
import json
import sys

def send_command(host, port, command, *args):
    """Send a command to the server and print the response."""
    try:
        # Create a socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            
            # Prepare the command data
            data = {"command": command, "args": args}
            
            # If the command is 'upload', read the file and include its content
            if command == "upload" and len(args) > 0:
                try:
                    # The first argument is the local file path
                    local_path = args[0]
                    # The second argument (if exists) is the remote filename
                    remote_filename = args[1] if len(args) > 1 else os.path.basename(local_path)
                    
                    with open(local_path, 'rb') as f:
                        file_content = f.read().decode('utf-8')
                    
                    # Set the file content in the data
                    data["file_content"] = file_content
                    # The first argument should be the remote filename
                    data["args"] = [remote_filename]
                    
                    print(f"[DEBUG] Uploading {local_path} as {remote_filename} (size: {len(file_content)} bytes)")
                except Exception as e:
                    print(f"Error reading file {args[0]}: {e}")
                    return
            
            message = json.dumps(data).encode('utf-8')
            
            # Send message length first (4 bytes)
            message_length = len(message).to_bytes(4, 'big')
            s.sendall(message_length + message)
            
            # Receive the response
            raw_msglen = s.recv(4)
            if not raw_msglen:
                print("No response from server")
                return
                
            msglen = int.from_bytes(raw_msglen, 'big')
            data = b''
            while len(data) < msglen:
                packet = s.recv(msglen - len(data))
                if not packet:
                    break
                data += packet
            
            # Print raw response data for debugging
            print(f"\n=== Raw Response ===")
            print(f"Raw data: {data}")
            print(f"Length: {len(data)} bytes")
            print("==================\n")
            
            try:
                # Try to parse as JSON
                response = json.loads(data.decode('utf-8'))
                print(f"\n=== Parsed Response ===")
                print(f"Status: {response.get('status')}")
                print(f"Message: {response.get('message')}")
                print("======================\n")
            except json.JSONDecodeError as e:
                print(f"Failed to parse response as JSON: {e}")
                print(f"Raw content: {data.decode('utf-8', errors='replace')}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python test_client.py <command> [args...]")
        print("Example: python test_client.py ls .")
        sys.exit(1)
    
    HOST = "127.0.0.1"
    PORT = 9996  # Default port, can be overridden with --port argument
    
    # Check for --port argument
    if "--port" in sys.argv:
        port_index = sys.argv.index("--port") + 1
        if port_index < len(sys.argv):
            PORT = int(sys.argv[port_index])
    
    command = sys.argv[1]
    args = sys.argv[2:] if len(sys.argv) > 2 else []
    
    print(f"Sending command: {command} {args}")
    send_command(HOST, PORT, command, *args)
