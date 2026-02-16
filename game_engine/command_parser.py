# Command Parser
# Parses user input into structured commands

from typing import NamedTuple, Dict, List, Optional, Tuple


class ParsedCommand(NamedTuple):
    """
    ParsedCommand represents a parsed user command.
    
    Attributes:
        command: The main command (e.g., "move", "take")
        args: List of arguments (e.g., ["north"], ["health_potion"])
        raw: The original raw input string
    """
    command: str
    args: list
    raw: str


class CommandParser:
    """
    CommandParser handles parsing user input into game commands.
    
    How it works:
    1. User enters a string like "move north" or "take sword"
    2. Parser cleans and splits the input
    3. Returns a ParsedCommand with command and arguments
    
    Supported commands:
    - move [direction] - Navigate to adjacent location
    - look - Describe current location  
    - take [item] - Pick up an item
    - drop [item] - Drop an item
    - use [item] - Use an item
    - inventory / i - Show inventory
    - stats / s - Show player stats
    - attack [target] - Attack an enemy
    - help - Show available commands
    
    Command aliases:
    - inventory = i
    - stats = s
    """
    
    # Command definitions: command name -> list of argument names
    COMMANDS = {
        'move': ['direction'],
        'look': [],
        'take': ['item_name'],
        'drop': ['item_name'],
        'use': ['item_name'],
        'inventory': [],
        'i': [],
        'stats': [],
        's': [],
        'attack': ['target'],
        'help': [],
        'save': [],
        'load': []
    }
    
    # Aliases mapping
    ALIASES = {
        'i': 'inventory',
        's': 'stats'
    }
    
    # Valid directions
    VALID_DIRECTIONS = ['north', 'south', 'east', 'west', 'up', 'down']
    
    def __init__(self):
        self._command_history: List[ParsedCommand] = []
    
    def parse(self, input_string: str) -> ParsedCommand:
        """
        Parse a user input string into a command.
        
        Args:
            input_string: The raw user input
            
        Returns:
            ParsedCommand with command, args, and raw input
        """
        # Store in history
        self._command_history.append(input_string)
        
        # Clean input: strip whitespace and convert to lowercase
        cleaned = input_string.strip().lower()
        
        # Handle empty input
        if not cleaned:
            return ParsedCommand("", [], input_string)
        
        # Split into parts
        parts = cleaned.split()
        
        # First word is the command
        command = parts[0]
        args = parts[1:]
        
        # Resolve aliases
        command = self.ALIASES.get(command, command)
        
        return ParsedCommand(command, args, input_string)
    
    def validate_command(self, parsed: ParsedCommand) -> Tuple[bool, Optional[str]]:
        """
        Validate a parsed command.
        
        Args:
            parsed: The parsed command to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        command = parsed.command
        
        # Check if command exists
        if command and command not in self.COMMANDS:
            return False, f"Unknown command: '{command}'. Type 'help' for available commands."
        
        if not command:
            return False, "Please enter a command."
        
        # Get expected arguments for this command
        expected_args = self.COMMANDS.get(command, [])
        
        # Check argument count
        if len(parsed.args) < len(expected_args):
            # Get argument name for error message
            if expected_args:
                arg_name = expected_args[len(parsed.args)]
                return False, f"Missing argument: {arg_name}"
            else:
                return False, f"Command '{command}' doesn't take any arguments."
        
        # Validate direction for move command
        if command == 'move':
            direction = parsed.args[0] if parsed.args else ""
            if direction not in self.VALID_DIRECTIONS:
                return False, f"Invalid direction: '{direction}'. Valid: {', '.join(self.VALID_DIRECTIONS)}"
        
        return True, None
    
    def get_available_commands(self) -> Dict[str, List[str]]:
        """
        Get all available commands and their arguments.
        
        Returns:
            Dictionary of commands and their arguments
        """
        return self.COMMANDS.copy()
    
    def get_command_help(self, command: str = None) -> str:
        """
        Get help text for a command or all commands.
        
        Args:
            command: Specific command to get help for, or None for all
            
        Returns:
            Help text string
        """
        if command:
            # Help for specific command
            if command in self.COMMANDS:
                args = self.COMMANDS[command]
                if args:
                    return f"{command} {' '.join(args)} - Use {command} with {', '.join(args)}"
                else:
                    return f"{command} - No arguments needed"
            elif command in self.ALIASES:
                real_command = self.ALIASES[command]
                return f"{command} is an alias for {real_command}"
            else:
                return f"Unknown command: {command}"
        else:
            # General help
            help_text = "Available commands:\n"
            for cmd, args in self.COMMANDS.items():
                if args:
                    help_text += f"  {cmd} <{', '.join(args)}>\n"
                else:
                    help_text += f"  {cmd}\n"
            return help_text
    
    def get_history(self) -> List[ParsedCommand]:
        """
        Get command history.
        
        Returns:
            List of parsed commands
        """
        return self._command_history.copy()


# Create global parser instance
parser = CommandParser()

