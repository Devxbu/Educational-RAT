import socket
import json
import os
import threading
import time
from typing import Dict, Any, Optional, Callable, Tuple

from utils import constants
from commands.base_command import CommandHandler
from commands.file_commands import register_file_commands
from commands.system_commands import register_system_commands
from commands.network_commands import register_network_commands
from commands.camera_commands import register_camera_commands

class Server:
    """Handles server-side network operations and command dispatching."""
    
    def __init__(self, host: str = constants.HOST, port: int = constants.PORT):
        """Initialize the server with the given host and port."""
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False
        self.clients = {}
        self.command_handler = CommandHandler()
        
        # Register all command handlers
        self._register_commands()
    
    def _register_commands(self) -> None:
        """Register all available commands with the command handler."""
        register_file_commands(self.command_handler)
        register_system_commands(self.command_handler)
        register_network_commands(self.command_handler)
        register_camera_commands(self.command_handler)
    
    def start(self) -> None:
        """Start the server and begin accepting connections."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(1)  # Allow for periodic checks of self.running
            
            self.running = True
            print(f"Server started on {self.host}:{self.port}")
            
            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    client_thread = threading.Thread(
                        target=self._handle_client,
                        args=(client_socket, client_address),
                        daemon=True
                    )
                    client_thread.start()
                    self.clients[client_address] = {
                        'socket': client_socket,
                        'thread': client_thread,
                        'active': True
                    }
                except socket.timeout:
                    continue
                except OSError as e:
                    if self.running:
                        print(f"Error accepting connection: {e}")
                    break
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the server and close all connections."""
        self.running = False
        
        # Close all client connections
        for client_info in self.clients.values():
            try:
                client_info['socket'].close()
            except:
                pass
        
        # Close the server socket
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        
        print("Server stopped")
    
    def _handle_client(self, client_socket: socket.socket, client_address: tuple) -> None:
        """Handle communication with a connected client."""
        print(f"New connection from {client_address}")
        
        # Initialize client state
        client_state = {
            'current_dir': os.getcwd()
        }
        
        try:
            while self.running:
                # Receive message length (first 4 bytes)
                raw_msglen = self._recv_all(client_socket, 4)
                if not raw_msglen:
                    break
                    
                msglen = int.from_bytes(raw_msglen, 'big')
                
                # Receive the actual message
                data = self._recv_all(client_socket, msglen)
                if not data:
                    break
                
                # Parse and process the command
                try:
                    command_data = json.loads(data.decode('utf-8'))
                    command = command_data.get('command', '')
                    args = command_data.get('args', [])
                    
                    # Store the current directory before executing the command
                    original_dir = os.getcwd()
                    
                    # Change to the client's current directory
                    if 'current_dir' in client_state:
                        os.chdir(client_state['current_dir'])
                    
                    # Execute the command with any additional kwargs from the command data
                    success, message = self.command_handler.execute_command(command, *args, **{k: v for k, v in command_data.items() if k not in ['command', 'args']})
                    
                    # Update the client's current directory if it was a cd command
                    if command == 'cd' and success:
                        client_state['current_dir'] = os.getcwd()
                    
                    # Change back to the original directory
                    os.chdir(original_dir)
                    
                    # Send the response
                    response = {
                        'status': 'success' if success else 'error',
                        'message': message
                    }
                    self._send_response(client_socket, response)
                    
                    # If it was an exit command, close the connection
                    if command == 'exit':
                        break
                        
                except json.JSONDecodeError:
                    self._send_error(client_socket, "Invalid JSON format")
                except Exception as e:
                    self._send_error(client_socket, f"Error processing command: {e}")
        
        except (ConnectionResetError, BrokenPipeError):
            print(f"Client {client_address} disconnected unexpectedly")
        except Exception as e:
            print(f"Error with client {client_address}: {e}")
        finally:
            client_socket.close()
            if client_address in self.clients:
                del self.clients[client_address]
            print(f"Connection closed: {client_address}")
    
    def _recv_all(self, sock: socket.socket, n: int) -> bytes:
        """Helper method to receive exactly n bytes from the socket."""
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return bytes(data)
    
    def _send_response(self, sock: socket.socket, data: Dict[str, Any]) -> None:
        """Send a JSON response to the client."""
        try:
            message = json.dumps(data).encode('utf-8')
            message_length = len(message).to_bytes(4, 'big')
            sock.sendall(message_length + message)
        except Exception as e:
            print(f"Error sending response: {e}")
    
    def _send_error(self, sock: socket.socket, message: str) -> None:
        """Send an error response to the client."""
        self._send_response(sock, {'status': 'error', 'message': message})

def start_server(host: str = None, port: int = None) -> Server:
    """Helper function to create and start a server instance."""
    host = host or constants.HOST
    port = port or constants.PORT
    
    server = Server(host, port)
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    
    return server
