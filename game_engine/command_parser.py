from typing import NamedTuple

class ParsedCommand(NamedTuple):
    command: str
    args: list 
    raw: str 

class CommandParser:
    COMMANDS = {
        'move': ['direction'],
        'look':[],
        'take':['item_name'],
        'drop':[],
        'use':[],
        'inventory':[],
        'attack':[],
        'help':[]
    }

    def parse(self,input_string:str) -> ParsedCommand:
        cleaned = input_string.strip().lower()

        parts = cleaned.split()

        if not parts:
            return ParsedCommand("",[],input_string)

        command = parts[0]
        args = parts[1:]

        return ParsedCommand(command, args, input_string)
