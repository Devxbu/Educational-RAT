import os
import requests
from typing import List, Tuple

from commands.base_command import Command
from utils import constants, helpers

class UploadCommand(Command):
    """Upload a file to the server."""
    
    @property
    def name(self) -> str:
        return "upload"
    
    def execute(self, *args, **kwargs) -> Tuple[bool, str]:
        # If file_content is provided in kwargs, it's a direct file upload
        if 'file_content' in kwargs:
            file_content = kwargs['file_content']
            print(f"[DEBUG] Received direct file content (length: {len(file_content)}): {file_content[:100]}...")
            
            # The first argument is the remote filename
            if len(args) > 0:
                remote_name = os.path.basename(args[0]) or 'uploaded_file.txt'
            else:
                remote_name = 'uploaded_file.txt'
                
            print(f"[DEBUG] Remote filename: {remote_name}")
            
            # Save the file content to the current working directory
            save_path = os.path.abspath(remote_name)
            save_dir = os.path.dirname(save_path)
            
            # Create directory if it doesn't exist
            if save_dir and not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
            
            print(f"[DEBUG] Saving to: {save_path}")
            
            try:
                with open(save_path, 'w', encoding='utf-8') as f:
                    f.write(file_content)
                print(f"[DEBUG] File saved successfully to {save_path}")
                return True, f"File uploaded successfully to: {save_path}"
            except Exception as e:
                print(f"[DEBUG] Error saving file: {e}")
                return False, f"Error saving file: {e}"
        
        # Otherwise, read from local file (for backward compatibility)
        local_path = args[0]
        remote_name = args[1] if len(args) > 1 else os.path.basename(local_path)
        
        try:
            if not os.path.isfile(local_path):
                return False, f"File not found: {local_path}"
            
            # Read the file content
            with open(local_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            
            # Save the file in the current directory
            save_path = os.path.join(os.getcwd(), remote_name)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                f.write(file_content)
            
            return True, f"File uploaded successfully as: {save_path}"
            
        except Exception as e:
            return False, f"Error during upload: {e}"

class DownloadCommand(Command):
    """Download a file from the server."""
    
    @property
    def name(self) -> str:
        return "download"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if len(args) < 1:
            return False, "Usage: download <file_path> [save_name]"
            
        file_path = args[0]
        save_name = args[1] if len(args) > 1 else os.path.basename(file_path)
        
        try:
            if not os.path.isfile(file_path):
                return False, f"File not found: {file_path}"
                
            # Read the file content
            with open(file_path, 'rb') as f:
                file_content = f.read()
            
            # Save the file with the new name in the current directory
            save_path = os.path.join(os.getcwd(), save_name)
            
            with open(save_path, 'wb') as f:
                f.write(file_content)
            
            return True, f"File downloaded successfully to {save_path}"
            
        except Exception as e:
            return False, f"Error during download: {e}"

class UploadFolderCommand(Command):
    """Upload a folder to the server."""
    
    @property
    def name(self) -> str:
        return "upload_folder"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if len(args) < 1:
            return False, "Usage: upload_folder <local_folder_path> [remote_folder_name]"
            
        local_folder = args[0]
        remote_name = args[1] if len(args) > 1 else os.path.basename(os.path.normpath(local_folder))
        
        if not os.path.isdir(local_folder):
            return False, f"Folder not found: {local_folder}"
        
        # Create a temporary directory for the zip file
        temp_dir = tempfile.mkdtemp()
        temp_zip_path = os.path.join(temp_dir, f"{remote_name}.zip")
        
        try:
            # Create a zip file of the folder
            with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(local_folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(local_folder))
                        zipf.write(file_path, arcname)
            
            # Extract the zip file in the current directory
            extract_path = os.path.join(os.getcwd(), remote_name)
            os.makedirs(extract_path, exist_ok=True)
            
            with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_path)
            
            return True, f"Folder uploaded and extracted successfully to: {extract_path}"
                
        except Exception as e:
            return False, f"Error during folder upload: {e}"
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(temp_zip_path):
                    os.remove(temp_zip_path)
                if os.path.exists(temp_dir):
                    os.rmdir(temp_dir)
            except Exception as e:
                print(f"Warning: Error cleaning up temporary files: {e}")

def register_network_commands(handler):
    """Register all network-related commands with the command handler."""
    handler.register_command(UploadCommand())
    handler.register_command(DownloadCommand())
    handler.register_command(UploadFolderCommand())
