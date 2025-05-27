# Educational RAT (Remote Access Tool) Project

**DISCLAIMER:** This project is created for **EDUCATIONAL PURPOSES ONLY**. It is designed to demonstrate network programming, client-server architecture, and system interactions in Python. Using this tool without explicit permission on systems you don't own is illegal and unethical.

## Project Overview

This educational RAT project consists of three main components:
1. `listener.py` - The command and control server
2. `trojan.py` - The client component
3. `server/` - Web server for file operations

## Features

- Remote command execution
- File system operations (ls, cd, pwd, etc.)
- Screenshot capture
- Webcam capture
- File upload/download capabilities
- Directory operations
- Self-destruction capability

## Requirements

```
pyautogui>=0.9.54
opencv-python>=4.8.0
requests>=2.31.0
requests-toolbelt>=1.0.0
```

## Setup & Usage

1. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the web server (for file operations):
   ```bash
   cd server
   # Follow server setup instructions
   ```

3. Run the listener:
   ```bash
   python listener.py
   # Enter the desired port number when prompted
   ```

4. Run the client (in a test environment only):
   ```bash
   python trojan.py
   ```

## Project Structure

- `listener.py`: The control server that accepts connections and sends commands
- `trojan.py`: The client that executes commands and connects back to the listener
- `server/`: Web server component for handling file operations
- `requirements.txt`: Python package dependencies

## Educational Value

This project demonstrates:
- Socket programming in Python
- Client-server architecture
- File system operations
- System command execution
- HTTP requests and file transfers
- Computer vision integration
- Error handling and connection management

## Security Notice

This tool is designed for educational purposes to understand:
- Network security concepts
- Remote system administration
- Security vulnerabilities
- Ethical hacking principles

**DO NOT** use this tool on any system without explicit permission. Unauthorized use may be illegal and result in serious consequences.

## Legal Disclaimer

This project is provided for educational purposes only. The authors are not responsible for any misuse or damage caused by this program. Users are responsible for ensuring they comply with all applicable laws and regulations in their jurisdiction.
