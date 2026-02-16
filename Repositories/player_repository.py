# Player Repository
# Manages player characters in the game

from typing import Optional
from models.character import Character
from Repositories.base_repository import BaseRepository

class PlayerRepository(BaseRepository[Character]):
    """
    PlayerRepository handles all player-related data operations.
    
    In our RPG game, there will typically be one active player,
    but we support multiple players for future features like:
    - Player profiles
    - Multiplayer
    - Character switching
    
    Key responsibilities:
    - Create new player characters
    - Retrieve player by ID
    - Update player stats/inventory
    - Delete players
    """
    
    def __init__(self):
        super().__init__()
        # Initialize with a default player for testing
        self._create_default_player()
    
    def _create_default_player(self):
        """Create a default player for testing."""
        default_player = Character(
            id="player_1",
            name="Hero",
            description="A brave adventurer",
            health=100,
            mana=50,
            strength=10,
            level=1,
            experience=0
        )
        self.create("player_1", default_player)
    
    def get_player(self, player_id: str = "player_1") -> Optional[Character]:
        """
        Get a player by ID.
        
        Args:
            player_id: The player's unique identifier
            
        Returns:
            The player character if found
        """
        return self.get(player_id)
    
    def create_player(self, name: str, health: int = 100, mana: int = 50, 
                      strength: int = 10) -> Character:
        """
        Create a new player character.
        
        Args:
            name: Player's name
            health: Starting health points
            mana: Starting mana points
            strength: Starting strength
            
        Returns:
            The newly created player
        """
        player_id = f"player_{len(self._storage) + 1}"
        player = Character(
            id=player_id,
            name=name,
            description=f"A brave adventurer named {name}",
            health=health,
            mana=mana,
            strength=strength,
            level=1,
            experience=0
        )
        return self.create(player_id, player)
    
    def update_player_stats(self, player_id: str, health: int = None, 
                           mana: int = None, strength: int = None,
                           level: int = None, experience: int = None) -> Optional[Character]:
        """
        Update a player's statistics.
        
        Args:
            player_id: The player's unique identifier
            health: New health value (optional)
            mana: New mana value (optional)
            strength: New strength value (optional)
            level: New level (optional)
            experience: New experience points (optional)
            
        Returns:
            Updated player if found
        """
        player = self.get(player_id)
        if player:
            if health is not None:
                player.health = health
            if mana is not None:
                player.mana = mana
            if strength is not None:
                player.strength = strength
            if level is not None:
                player.level = level
            if experience is not None:
                player.experience = experience
            return self.update(player_id, player)
        return None
    
    def add_experience(self, player_id: str, exp: int) -> Optional[Character]:
        """
        Add experience points to a player and handle leveling up.
        
        Args:
            player_id: The player's unique identifier
            exp: Experience points to add
            
        Returns:
            Updated player if found
        """
        player = self.get(player_id)
        if player:
            player.experience += exp
            
            # Level up logic: 100 XP per level
            new_level = (player.experience // 100) + 1
            if new_level > player.level:
                player.level = new_level
                # Bonus stats on level up
                player.health += 10
                player.mana += 5
                player.strength += 2
            
            return self.update(player_id, player)
        return None
    
    def take_damage(self, player_id: str, damage: int) -> Optional[Character]:
        """
        Apply damage to a player.
        
        Args:
            player_id: The player's unique identifier
            damage: Amount of damage to take
            
        Returns:
            Updated player if found
        """
        player = self.get(player_id)
        if player:
            player.health = max(0, player.health - damage)
            return self.update(player_id, player)
        return None
    
    def heal(self, player_id: str, amount: int) -> Optional[Character]:
        """
        Heal a player.
        
        Args:
            player_id: The player's unique identifier
            amount: Amount to heal
            
        Returns:
            Updated player if found
        """
        player = self.get(player_id)
        if player:
            player.health = min(player.health + amount, player.max_health)
            return self.update(player_id, player)
        return None

