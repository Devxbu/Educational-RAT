import socket
import json
from typing import Any, Dict, Optional, Tuple

from utils import constants

class Client:
    """Handles client-side network operations."""
    
    def __init__(self, host: str = constants.HOST, port: int = constants.PORT):
        """Initialize the client with server connection details."""
        self.host = host
        self.port = port
        self.socket = None
        self.connected = False
    
    def connect(self) -> bool:
        """Establish a connection to the server."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 seconds timeout
            self.socket.connect((self.host, self.port))
            self.connected = True
            return True
        except (socket.error, socket.timeout) as e:
            print(f"Connection error: {e}")
            self.connected = False
            return False
    
    def send_command(self, command: str, *args) -> Optional[Dict[str, Any]]:
        """Send a command to the server and wait for a response."""
        if not self.connected and not self.connect():
            return {"status": "error", "message": "Failed to connect to server"}
        
        try:
            # Prepare the command data
            data = {"command": command, "args": args}
            message = json.dumps(data).encode('utf-8')
            
            # Send message length first
            message_length = len(message).to_bytes(4, 'big')
            self.socket.sendall(message_length + message)
            
            # Wait for response
            return self._receive_response()
            
        except (socket.error, json.JSONDecodeError) as e:
            self.connected = False
            return {"status": "error", "message": f"Communication error: {e}"}
    
    def _receive_response(self) -> Optional[Dict[str, Any]]:
        """Receive a response from the server."""
        try:
            # Get the message length (first 4 bytes)
            raw_msglen = self._recvall(4)
            if not raw_msglen:
                return None
                
            msglen = int.from_bytes(raw_msglen, 'big')
            
            # Get the actual message
            data = self._recvall(msglen)
            if not data:
                return None
                
            return json.loads(data.decode('utf-8'))
            
        except (socket.error, json.JSONDecodeError) as e:
            self.connected = False
            return {"status": "error", "message": f"Error receiving response: {e}"}
    
    def _recvall(self, n: int) -> bytes:
        """Helper method to receive n bytes or return None if connection is closed."""
        data = bytearray()
        while len(data) < n:
            packet = self.socket.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)
    
    def close(self) -> None:
        """Close the connection."""
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            finally:
                self.socket = None
                self.connected = False
    
    def __del__(self):
        """Ensure the socket is closed when the object is destroyed."""
        self.close()


def send_file(host: str, port: int, file_path: str) -> Dict[str, Any]:
    """Utility function to send a file to the server."""
    client = Client(host, port)
    try:
        with open(file_path, 'rb') as f:
            file_data = f.read()
        return client.send_command("upload", os.path.basename(file_path), file_data)
    except Exception as e:
        return {"status": "error", "message": f"Failed to send file: {e}"}
    finally:
        client.close()

def receive_file(host: str, port: int, file_name: str, save_path: str) -> Dict[str, Any]:
    """Utility function to receive a file from the server."""
    client = Client(host, port)
    try:
        response = client.send_command("download", file_name)
        if response and response.get("status") == "success":
            with open(save_path, 'wb') as f:
                f.write(response.get("data", b""))
            return {"status": "success", "message": f"File saved to {save_path}"}
        return response or {"status": "error", "message": "No response from server"}
    except Exception as e:
        return {"status": "error", "message": f"Failed to receive file: {e}"}
    finally:
        client.close()
