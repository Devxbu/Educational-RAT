import os

# Network configuration
HOST = "127.0.0.1"
PORT = 9991

# File paths
FILE_DIR = os.getcwd()
FILE_NAME = os.path.basename(__file__)

# Server endpoints
SERVER_BASE_URL = "http://localhost:8000/api"
SERVER_FILE_URL = f"{SERVER_BASE_URL}/file"
SERVER_FOLDER_URL = f"{SERVER_BASE_URL}/folder"

# File operations
BUFFER_SIZE = 8192  # For file transfers

# Default values
DEFAULT_SCREENSHOT_NAME = "screenshot_{timestamp}.png"
DEFAULT_CAMERA_CAPTURE_NAME = "camera_capture_{timestamp}.jpg"
