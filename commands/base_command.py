from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Tuple

class Command(ABC):
    """Base class for all command handlers."""
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> Tuple[bool, str]:
        """
        Execute the command with the given arguments.
        
        Args:
            *args: Variable length argument list for the command.
            **kwargs: Keyword arguments for the command.
            
        Returns:
            Tuple[bool, str]: A tuple containing:
                - success (bool): Whether the command executed successfully
                - message (str): The result message or error message
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the name of the command."""
        pass
    
    @property
    def requires_connection(self) -> bool:
        """
        Whether this command requires an active connection to the server.
        
        Returns:
            bool: True if connection is required, False otherwise
        """
        return False


class CommandHandler:
    """Manages command registration and execution."""
    
    def __init__(self):
        self._commands: Dict[str, Command] = {}
    
    def register_command(self, command: Command) -> None:
        """Register a command handler."""
        self._commands[command.name] = command
    
    def execute_command(self, command_name: str, *args, **kwargs) -> Tuple[bool, str]:
        """
        Execute a command by name with the given arguments.
        
        Args:
            command_name: Name of the command to execute
            *args: Positional arguments to pass to the command
            **kwargs: Keyword arguments to pass to the command
            
        Returns:
            Tuple[bool, str]: The result of the command execution
        """
        if command_name not in self._commands:
            return False, f"Unknown command: {command_name}"
            
        command = self._commands[command_name]
        
        try:
            return command.execute(*args, **kwargs)
        except Exception as e:
            return False, f"Error processing command: {str(e)}"
    
    def get_available_commands(self) -> List[str]:
        """Get a list of all registered command names."""
        return list(self._commands.keys())
    
    def command_exists(self, command_name: str) -> bool:
        """Check if a command with the given name exists."""
        return command_name.lower() in self._commands
