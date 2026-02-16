# Game State Repository
# Manages the overall game state including player position, inventory, world, etc.

from typing import Optional, Dict, Any
from dataclasses import dataclass, field, asdict
from models.location import Location
from models.item import Item
from models.character import Character

@dataclass
class GameStateData:
    """
    GameStateData holds all the information about the current game session.
    
    This includes:
    - Player information
    - Current location
    - Player's inventory
    - Game status (playing, combat, game_over)
    - Visited locations
    - World data (all locations)
    """
    player_id: str = "player_1"
    current_location_id: str = "start"
    inventory: list = field(default_factory=list)  # List of item IDs
    game_status: str = "playing"  # playing, combat, game_over, paused
    visited_locations: set = field(default_factory=set)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "player_id": self.player_id,
            "current_location_id": self.current_location_id,
            "inventory": self.inventory,
            "game_status": self.game_status,
            "visited_locations": list(self.visited_locations)
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'GameStateData':
        """Create from dictionary."""
        visited = set(data.get("visited_locations", []))
        return cls(
            player_id=data.get("player_id", "player_1"),
            current_location_id=data.get("current_location_id", "start"),
            inventory=data.get("inventory", []),
            game_status=data.get("game_status", "playing"),
            visited_locations=visited
        )


class GameStateRepository:
    """
    GameStateRepository manages the current game state.
    
    Responsibilities:
    - Save and load game state
    - Track player position in the world
    - Manage inventory state
    - Handle game status (playing, combat, game_over)
    
    In a full implementation, this would persist to disk/database.
    For now, we use in-memory storage.
    """
    
    def __init__(self):
        # Current game state
        self._current_state: Optional[GameStateData] = None
        
        # Saved games - in memory for now (could be files/database)
        self._saved_games: Dict[str, GameStateData] = {}
    
    def initialize_new_game(self, player_id: str = "player_1") -> GameStateData:
        """
        Initialize a new game state.
        
        Args:
            player_id: The player's unique identifier
            
        Returns:
            The new game state
        """
        self._current_state = GameStateData(
            player_id=player_id,
            current_location_id="start",
            inventory=[],
            game_status="playing",
            visited_locations=set()
        )
        return self._current_state
    
    def get_current_state(self) -> Optional[GameStateData]:
        """
        Get the current game state.
        
        Returns:
            Current game state or None if no game in progress
        """
        return self._current_state
    
    def update_location(self, location_id: str) -> bool:
        """
        Update the player's current location.
        
        Args:
            location_id: The new location ID
            
        Returns:
            True if updated successfully
        """
        if self._current_state:
            self._current_state.current_location_id = location_id
            self._current_state.visited_locations.add(location_id)
            return True
        return False
    
    def add_item_to_inventory(self, item_id: str) -> bool:
        """
        Add an item to player's inventory.
        
        Args:
            item_id: The item's unique identifier
            
        Returns:
            True if added successfully
        """
        if self._current_state:
            if item_id not in self._current_state.inventory:
                self._current_state.inventory.append(item_id)
                return True
        return False
    
    def remove_item_from_inventory(self, item_id: str) -> bool:
        """
        Remove an item from player's inventory.
        
        Args:
            item_id: The item's unique identifier
            
        Returns:
            True if removed successfully
        """
        if self._current_state:
            if item_id in self._current_state.inventory:
                self._current_state.inventory.remove(item_id)
                return True
        return False
    
    def get_inventory(self) -> list:
        """
        Get player's inventory.
        
        Returns:
            List of item IDs in inventory
        """
        if self._current_state:
            return self._current_state.inventory.copy()
        return []
    
    def set_game_status(self, status: str) -> bool:
        """
        Set the game status.
        
        Args:
            status: New game status (playing, combat, game_over, paused)
            
        Returns:
            True if updated successfully
        """
        if self._current_state:
            valid_statuses = ["playing", "combat", "game_over", "paused"]
            if status in valid_statuses:
                self._current_state.game_status = status
                return True
        return False
    
    def save_game(self, save_name: str = "autosave") -> bool:
        """
        Save the current game state.
        
        Args:
            save_name: Name for this save
            
        Returns:
            True if saved successfully
        """
        if self._current_state:
            self._saved_games[save_name] = GameStateData.from_dict(
                self._current_state.to_dict()
            )
            return True
        return False
    
    def load_game(self, save_name: str = "autosave") -> Optional[GameStateData]:
        """
        Load a saved game.
        
        Args:
            save_name: Name of the save to load
            
        Returns:
            Loaded game state or None if not found
        """
        saved_state = self._saved_games.get(save_name)
        if saved_state:
            self._current_state = GameStateData.from_dict(saved_state.to_dict())
            return self._current_state
        return None
    
    def get_saved_games(self) -> list:
        """
        Get list of saved game names.
        
        Returns:
            List of save names
        """
        return list(self._saved_games.keys())
    
    def has_active_game(self) -> bool:
        """
        Check if there's an active game.
        
        Returns:
            True if there's an active game
        """
        return self._current_state is not None

