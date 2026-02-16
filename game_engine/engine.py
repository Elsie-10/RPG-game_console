from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
from models import Character, Location, Item
from event_manager import EventManager, PLAYER_MOVED, ITEM_PICKED_UP

@dataclass
class GameState:
    player: Character
    current_location: Location
    inventory: List[Item] = field(default_factory=list)
    game_status: str = 'playing'
    visited_locations: Set[str] = field(default_factory=set)

class GameEngine:
    def __init__(self):
        self.event_manager = EventManager()
        self.game_state = None
        self.world = {}
    
    def initialize_world(self):
        # Create locations
        # Create items
        # Set up exits
        # Set player starting position
        pass
    
    def process_command(self, parsed_command) -> dict:
        # Route to handler
        # Return response
        pass
    
    def handle_move(self, args: list) -> dict:
        # Check if direction exists in current_location.exits
        # If yes: update location, publish PLAYER_MOVED, return success
        # If no: return error message
        pass