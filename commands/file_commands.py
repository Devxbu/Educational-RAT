import os
import shutil
import zipfile
from typing import List, Tuple

from commands.base_command import Command
from utils import constants, helpers

class ChangeDirectoryCommand(Command):
    """Change the current working directory."""
    
    @property
    def name(self) -> str:
        return "cd"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if not args:
            return False, "No directory specified"
            
        try:
            target_dir = args[0]
            os.chdir(target_dir)
            return True, f"Changed directory to {os.getcwd()}"
        except Exception as e:
            return False, f"Error changing directory: {e}"

class PrintWorkingDirectoryCommand(Command):
    """Print the current working directory."""
    
    @property
    def name(self) -> str:
        return "pwd"
    
    def execute(self, *args) -> Tuple[bool, str]:
        try:
            return True, os.getcwd()
        except Exception as e:
            return False, f"Error getting current directory: {e}"

class ListDirectoryCommand(Command):
    """List contents of the current directory."""
    
    @property
    def name(self) -> str:
        return "ls"
    
    def execute(self, *args) -> Tuple[bool, str]:
        try:
            path = args[0] if args else "."
            entries = os.listdir(path)
            return True, "\n".join(entries)
        except Exception as e:
            return False, f"Error listing directory: {e}"

class MakeDirectoryCommand(Command):
    """Create a new directory."""
    
    @property
    def name(self) -> str:
        return "mkdir"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if not args:
            return False, "No directory name specified"
            
        try:
            os.makedirs(args[0], exist_ok=True)
            return True, f"Created directory: {args[0]}"
        except Exception as e:
            return False, f"Error creating directory: {e}"

class RemoveCommand(Command):
    """Remove a file or directory."""
    
    @property
    def name(self) -> str:
        return "rm"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if not args:
            return False, "No file or directory specified"
            
        target = args[0]
        try:
            if os.path.isfile(target):
                os.remove(target)
                return True, f"Removed file: {target}"
            elif os.path.isdir(target):
                shutil.rmtree(target)
                return True, f"Removed directory: {target}"
            else:
                return False, f"No such file or directory: {target}"
        except Exception as e:
            return False, f"Error removing {target}: {e}"

class ReadFileCommand(Command):
    """Read the contents of a file."""
    
    @property
    def name(self) -> str:
        return "cat"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if not args:
            return False, "No file specified"
            
        try:
            with open(args[0], 'r') as f:
                return True, f.read()
        except Exception as e:
            return False, f"Error reading file: {e}"

class TouchCommand(Command):
    """Create an empty file."""
    
    @property
    def name(self) -> str:
        return "touch"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if not args:
            return False, "No file specified"
            
        try:
            with open(args[0], 'a'):
                os.utime(args[0], None)
            return True, f"Created file: {args[0]}"
        except Exception as e:
            return False, f"Error creating file: {e}"

class UnzipCommand(Command):
    """Extract a zip archive."""
    
    @property
    def name(self) -> str:
        return "unzip"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if len(args) < 1:
            return False, "Usage: unzip <archive> [destination]"
            
        archive = args[0]
        dest = args[1] if len(args) > 1 else "."
        
        try:
            with zipfile.ZipFile(archive, 'r') as zip_ref:
                zip_ref.extractall(dest)
            return True, f"Extracted {archive} to {dest}"
        except Exception as e:
            return False, f"Error extracting {archive}: {e}"

def register_file_commands(handler):
    """Register all file-related commands with the command handler."""
    commands = [
        ChangeDirectoryCommand(),
        ListDirectoryCommand(),
        MakeDirectoryCommand(),
        RemoveCommand(),
        ReadFileCommand(),
        TouchCommand(),
        UnzipCommand(),
        PrintWorkingDirectoryCommand()
    ]
    
    for cmd in commands:
        print(f"Registering command: {cmd.name}")
        handler.register_command(cmd)
