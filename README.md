# Educational RAT - Remote Administration Tool

A modular remote administration tool with a client-server architecture, providing various system administration capabilities over a network connection. This project is designed for educational purposes and authorized system administration only.

**⚠️ IMPORTANT: This tool is for educational and authorized use only. Unauthorized access to computer systems is illegal.**

## ✨ Features

- **File Operations**: List, view, create, delete, and modify files and directories
- **System Control**: Execute shell commands, take screenshots, capture webcam
- **Network Operations**: Upload/download files and folders with progress tracking
- **Modular Design**: Easy to extend with new commands and functionality
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Persistent Connections**: Maintains connection state and current directory per client

## Project Structure

```
RAT-4.0/
├── commands/               # Command implementations
│   ├── __init__.py
│   ├── base_command.py     # Base command classes
│   ├── file_commands.py    # File system commands
│   ├── system_commands.py  # System control commands
│   ├── network_commands.py # Network operations
│   └── camera_commands.py  # Camera-related commands
├── network/               # Network communication
│   ├── __init__.py
│   ├── server.py          # Server implementation
│   └── client.py          # Client implementation
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── constants.py       # Constants and configuration
│   └── helpers.py         # Helper functions
├── test_client.py         # Test client for development
├── main.py               # Main entry point
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Devxbu/Educational-RAT.git
   cd Educational-RAT
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   # On macOS/Linux
   python3 -m venv venv
   source venv/bin/activate

   # On Windows
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Configuration

1. Edit `utils/constants.py` to configure default settings:
   ```python
   DEFAULT_HOST = '127.0.0.1'  # Default binding address
   DEFAULT_PORT = 9999         # Default port
   BUFFER_SIZE = 4096          # Network buffer size
   ```

## 🖥️ Usage

### Starting the Server

```bash
python main.py [--host HOST] [--port PORT] [--debug]
```

- `--host`: Host to bind to (default: 127.0.0.1)
- `--port`: Port to listen on (default: 9999)
- `--debug`: Enable debug output (useful for development)

### 🧪 Using the Test Client

The test client (`test_client.py`) is a command-line interface for interacting with the RAT server. It's designed for development and testing purposes.

#### Basic Usage

```bash
# Connect to a server and execute a command
python test_client.py <command> [args...]

# Example: List files in the root directory
python test_client.py ls /

# Example: Change directory
python test_client.py cd /path/to/directory
```

#### File Operations

```bash
# Upload a file to the server
python test_client.py upload /local/path/file.txt [remote_name.txt]

# Download a file from the server
python test_client.py download remote_file.txt [local_path]

# Upload an entire folder (will be zipped)
python test_client.py upload_folder /local/folder [remote_name.zip]
```

#### System Commands

```bash
# Execute a shell command
python test_client.py exec "ls -la"

# Take a screenshot
python test_client.py screenshot [output.jpg]

# Capture from webcam
python test_client.py camera_capture [output.jpg]
```

#### Advanced Usage

```bash
# Connect to a custom host and port
python test_client.py --host 192.168.1.100 --port 9999 ls /

# Get help
python test_client.py help

# List all available commands
python test_client.py list_commands
```

#### Command Line Options

- `--host`: Server hostname or IP (default: 127.0.0.1)
- `--port`: Server port (default: 9999)
- `--debug`: Enable debug output

### Available Commands

Run `python test_client.py help` to see all available commands.

### Available Commands

#### File Operations
- `ls [path]` - List directory contents
- `cd <directory>` - Change directory
- `mkdir <directory>` - Create a new directory
- `rm <file/directory>` - Remove a file or directory
- `cat <file>` - View file contents
- `touch <file>` - Create an empty file
- `unzip <archive> [destination]` - Extract a zip archive

#### System Control
- `exit` - Exit the application
- `shutdown` - Shutdown the system
- `screenshot` - Take a screenshot
- `exec <command>` - Execute a shell command
- `selfdestruct` - Remove all traces of the application

#### Network Operations
- `upload <local_path> [remote_name]` - Upload a file
- `download <file_id> [save_path]` - Download a file
- `upload_folder <local_folder> [remote_name]` - Upload a folder

#### Camera
- `camera_capture` - Capture an image from the webcam
- `camera_stream [duration]` - Stream from the webcam (default: 10 seconds)

## ⚠️ Security and Legal Notice

**IMPORTANT:** This tool is designed **ONLY** for:
- Educational purposes
- Authorized system administration
- Security research with explicit permission

### Legal Requirements
- You **MUST** have explicit permission to run this tool on any system
- Unauthorized access to computer systems is illegal in most jurisdictions
- The developers assume **NO** liability for misuse of this software

### Security Best Practices
- Always run the server on trusted networks only
- Use strong authentication if exposing to untrusted networks
- Regularly update the software to the latest version
- Review the code before running in production environments

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Contact

For questions or concerns, please open an issue on the GitHub repository.

---

<div align="center">
  <sub>Built with ❤️ by Bahri URANLI</sub>
</div>
