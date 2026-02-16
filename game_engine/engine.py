from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set
import random

# Import models
from models.character import Character
from models.location import Location
from models.item import Item

# Import event system
from game_engine.event_manager import (
    EventManager, 
    PLAYER_MOVED, 
    ITEM_PICKED_UP, 
    ITEM_DROPPED,
    ITEM_USED,
    COMBAT_STARTED,
    COMBAT_ENDED,
    PLAYER_DAMAGED,
    PLAYER_HEALED,
    ENEMY_DEFEATED,
    ENEMY_DAMAGED,
    GAME_STARTED,
    LEVEL_UP
)


@dataclass
class GameState:
    """GameState holds all the information about the current game session."""
    player: Character
    current_location: Location
    inventory: List[Item] = field(default_factory=list)
    game_status: str = 'playing'
    visited_locations: Set[str] = field(default_factory=set)


class GameEngine:
    """GameEngine is the main controller for the game."""
    
    def __init__(self):
        self.event_manager = EventManager()
        self.game_state: Optional[GameState] = None
        self.world: Dict[str, Location] = {}
        self.items_db: Dict[str, Item] = {}
        
        from game_engine.command_parser import CommandParser
        self.parser = CommandParser()
        
        self._setup_event_listeners()
    
    def _setup_event_listeners(self):
        """Set up event listeners for game events."""
        self.event_manager.subscribe(PLAYER_MOVED, self._on_player_moved)
        self.event_manager.subscribe(ITEM_PICKED_UP, self._on_item_picked_up)
        self.event_manager.subscribe(ITEM_DROPPED, self._on_item_dropped)
        self.event_manager.subscribe(COMBAT_STARTED, self._on_combat_started)
        self.event_manager.subscribe(COMBAT_ENDED, self._on_combat_ended)
    
    def _on_player_moved(self, event):
        print(f"[EVENT] Player moved to: {event.data.get('location', 'unknown')}")
    
    def _on_item_picked_up(self, event):
        print(f"[EVENT] Player picked up: {event.data.get('item', 'unknown')}")
    
    def _on_item_dropped(self, event):
        print(f"[EVENT] Player dropped: {event.data.get('item', 'unknown')}")
    
    def _on_combat_started(self, event):
        print(f"[EVENT] Combat started with: {event.data.get('enemy', 'unknown')}")
    
    def _on_combat_ended(self, event):
        print(f"[EVENT] Combat ended. Result: {event.data.get('result', 'unknown')}")
    
    def initialize_world(self) -> GameState:
        """Initialize the game world with locations, items, and enemies."""
        # Create the player
        player = Character(
            id="player_1",
            name="Hero",
            description="A brave adventurer",
            health=100,
            mana=50,
            strength=10,
            level=1,
            experience=0
        )
        
        # Create items
        self._create_items()
        
        # Create locations
        self._create_locations()
        
        # Create initial game state
        start_location = self.world["start"]
        self.game_state = GameState(
            player=player,
            current_location=start_location,
            inventory=[],
            game_status='playing',
            visited_locations={'start'}
        )
        
        # Publish game started event
        self.event_manager.publish(GAME_STARTED, {"player": player.name})
        
        return self.game_state
    
    def _create_items(self):
        """Create all game items."""
        items_data = [
            Item("iron_sword", "Iron Sword", "A sturdy iron sword", "weapon", 10, {"attack": 5}, True),
            Item("magic_staff", "Magic Staff", "A staff imbued with magical power", "weapon", 50, {"attack": 15}, True),
            Item("wooden_shield", "Wooden Shield", "A basic wooden shield", "shield", 5, {"defense": 3}, True),
            Item("health_potion", "Health Potion", "Restores 30 health points", "potion", 10, {"heal": 30}, False),
            Item("mana_potion", "Mana Potion", "Restores 25 mana points", "potion", 10, {"mana": 25}, False),
            Item("strength_potion", "Strength Potion", "Temporarily increases strength by 5", "potion", 25, {"strength_boost": 5}, False),
            Item("gold_coin", "Gold Coin", "A shiny gold coin", "treasure", 1, {}, False),
            Item("ruby", "Ruby", "A precious red gem", "treasure", 100, {}, False),
            Item("ancient_scroll", "Ancient Scroll", "Contains mysterious knowledge", "treasure", 50, {}, False),
        ]
        
        for item in items_data:
            self.items_db[item.entity_id] = item
    
    def _create_locations(self):
        """Create all game world locations."""
        
        # Starting location - a clearing
        start = Location(
            id="start",
            name="Forest Clearing",
            description="You are in a peaceful forest clearing. Sunlight filters through the trees.",
            exits={"north": "forest", "east": "village"},
            items=["iron_sword", "wooden_shield"],
            enemies=[],
            is_locked=False
        )
        
        # Forest
        forest = Location(
            id="forest",
            name="Dark Forest",
            description="The trees are thick here and block most sunlight. You hear strange sounds.",
            exits={"south": "start", "north": "dungeon"},
            items=["health_potion", "strength_potion"],
            enemies=[{"id": "wolf", "name": "Wolf", "health": 30, "damage": 10}],
            is_locked=False
        )
        
        # Village
        village = Location(
            id="village",
            name="Village",
            description="A small peaceful village with thatched-roof houses. Villagers go about their daily business.",
            exits={"west": "start", "north": "cave"},
            items=["mana_potion", "gold_coin"],
            enemies=[],
            is_locked=False
        )
        
        # Dungeon
        dungeon = Location(
            id="dungeon",
            name="Dark Dungeon",
            description="A cold, dark dungeon. The walls are damp and you hear growling in the shadows.",
            exits={"south": "forest", "east": "treasure_room"},
            items=["magic_staff", "ruby"],
            enemies=[
                {"id": "goblin", "name": "Goblin", "health": 40, "damage": 15},
                {"id": "skeleton", "name": "Skeleton", "health": 35, "damage": 12}
            ],
            is_locked=False
        )
        
        # Cave
        cave = Location(
            id="cave",
            name="Mysterious Cave",
            description="A dark cave with glowing crystals on the walls. Ancient markings cover the walls.",
            exits={"south": "village"},
            items=["ancient_scroll", "health_potion"],
            enemies=[],
            is_locked=False
        )
        
        # Treasure room
        treasure_room = Location(
            id="treasure_room",
            name="Treasure Room",
            description="A magnificent chamber filled with gold and treasures! But beware - a dragon sleeps here.",
            exits={"west": "dungeon"},
            items=["gold_coin", "ruby", "ruby"],
            enemies=[{"id": "dragon", "name": "Dragon", "health": 100, "damage": 25}],
            is_locked=False
        )
        
        # Add all locations to world
        self.world = {
            "start": start,
            "forest": forest,
            "village": village,
            "dungeon": dungeon,
            "cave": cave,
            "treasure_room": treasure_room
        }
    
    def process_command(self, input_string: str) -> dict:
        """Process a player command."""
        if not self.game_state:
            return {"success": False, "message": "Game not initialized. Call initialize_world() first."}
        
        # Parse the command
        parsed = self.parser.parse(input_string)
        
        # Validate command
        is_valid, error_msg = self.parser.validate_command(parsed)
        if not is_valid:
            return {"success": False, "message": error_msg}
        
        # Route to appropriate handler
        command = parsed.command
        args = parsed.args
        
        handlers = {
            'move': self.handle_move,
            'look': self.handle_look,
            'take': self.handle_take,
            'drop': self.handle_drop,
            'use': self.handle_use,
            'inventory': self.handle_inventory,
            'stats': self.handle_stats,
            'attack': self.handle_attack,
            'help': self.handle_help,
            'save': self.handle_save,
            'load': self.handle_load
        }
        
        handler = handlers.get(command)
        if handler:
            return handler(args)
        else:
            return {"success": False, "message": f"Command '{command}' not implemented yet."}
    
    # ==================== COMMAND HANDLERS ====================
    
    def handle_move(self, args: list) -> dict:
        """Handle player movement."""
        if not args:
            return {"success": False, "message": "Move where? Specify a direction (north, south, east, west)."}
        
        direction = args[0].lower()
        current_loc = self.game_state.current_location
        
        # Check if direction exists
        if direction not in current_loc.exits:
            return {"success": False, "message": f"You can't go {direction}. Available exits: {', '.join(current_loc.exits.keys())}"}
        
        # Get new location ID
        new_location_id = current_loc.exits[direction]
        
        # Check if location exists
        if new_location_id not in self.world:
            return {"success": False, "message": "Something went wrong. That location doesn't exist."}
        
        # Get new location
        new_location = self.world[new_location_id]
        
        # Check if location is locked
        if new_location.is_locked:
            return {"success": False, "message": f"The {new_location.name} is locked. You need a key."}
        
        # Update player location
        self.game_state.current_location = new_location
        self.game_state.visited_locations.add(new_location_id)
        
        # Publish event
        self.event_manager.publish(PLAYER_MOVED, {
            "location": new_location_id,
            "direction": direction
        })
        
        return {
            "success": True, 
            "message": f"You head {direction}...\n\n{new_location.name}\n{new_location.description}",
            "data": {"location": new_location_id, "exits": list(new_location.exits.keys())}
        }
    
    def handle_look(self, args: list = None) -> dict:
        """Describe the current location."""
        location = self.game_state.current_location
        
        description = f"\n=== {location.name} ===\n\n{location.description}\n"
        
        if location.exits:
            exits_str = ", ".join(location.exits.keys())
            description += f"\nExits: {exits_str}"
        
        if location.items:
            items_in_location = [self.items_db[item_id].name for item_id in location.items if item_id in self.items_db]
            if items_in_location:
                description += f"\n\nYou see: {', '.join(items_in_location)}"
        
        if location.enemies:
            enemy_names = [e["name"] for e in location.enemies]
            description += f"\n\n⚔️ DANGER! Enemies here: {', '.join(enemy_names)}"
        
        return {"success": True, "message": description}
    
    def handle_take(self, args: list) -> dict:
        """Pick up an item from the current location."""
        if not args:
            return {"success": False, "message": "Take what? Specify an item name."}
        
        item_name = " ".join(args).lower()
        location = self.game_state.current_location
        
        # Find item in location
        found_item_id = None
        for item_id in location.items:
            if item_id in self.items_db:
                item = self.items_db[item_id]
                if item_name in item.name.lower() or item_name in item_id.lower():
                    found_item_id = item_id
                    break
        
        if not found_item_id:
            return {"success": False, "message": f"There's no '{item_name}' here."}
        
        # Remove from location
        location.items.remove(found_item_id)
        
        # Add to inventory
        item = self.items_db[found_item_id]
        self.game_state.inventory.append(item)
        
        # Publish event
        self.event_manager.publish(ITEM_PICKED_UP, {
            "item": item.name,
            "item_id": found_item_id
        })
        
        return {
            "success": True,
            "message": f"You pick up the {item.name}. {item.description}",
            "data": {"item": item.name}
        }
    
    def handle_drop(self, args: list) -> dict:
        """Drop an item from inventory to the current location."""
        if not args:
            return {"success": False, "message": "Drop what? Specify an item name."}
        
        item_name = " ".join(args).lower()
        
        # Find item in inventory
        found_item = None
        found_index = None
        for i, item in enumerate(self.game_state.inventory):
            if item_name in item.name.lower() or item_name in item.entity_id.lower():
                found_item = item
                found_index = i
                break
        
        if not found_item:
            return {"success": False, "message": f"You don't have a '{item_name}' in your inventory."}
        
        # Remove from inventory
        self.game_state.inventory.pop(found_index)
        
        # Add to location
        self.game_state.current_location.items.append(found_item.entity_id)
        
        # Publish event
        self.event_manager.publish(ITEM_DROPPED, {
            "item": found_item.name,
            "item_id": found_item.entity_id
        })
        
        return {
            "success": True,
            "message": f"You drop the {found_item.name}.",
            "data": {"item": found_item.name}
        }
    
    def handle_use(self, args: list) -> dict:
        """Use an item from inventory."""
        if not args:
            return {"success": False, "message": "Use what? Specify an item name."}
        
        item_name = " ".join(args).lower()
        
        # Find item in inventory
        found_item = None
        found_index = None
        for i, item in enumerate(self.game_state.inventory):
            if item_name in item.name.lower() or item_name in item.entity_id.lower():
                found_item = item
                found_index = i
                break
        
        if not found_item:
            return {"success": False, "message": f"You don't have a '{item_name}' in your inventory."}
        
        # Apply item effects
        player = self.game_state.player
        effect = found_item.effect or {}
        
        if not effect:
            return {"success": False, "message": f"The {found_item.name} can't be used."}
        
        messages = []
        
        # Health potion
        if "heal" in effect:
            heal_amount = effect["heal"]
            old_health = player.health
            player.health = min(player.health + heal_amount, player.max_health)
            actual_heal = player.health - old_health
            messages.append(f"You heal for {actual_heal} HP!")
            self.event_manager.publish(PLAYER_HEALED, {"amount": actual_heal})
        
        # Mana potion
        if "mana" in effect:
            mana_amount = effect["mana"]
            player.mana = min(player.mana + mana_amount, 100)
            messages.append(f"You restore {mana_amount} mana!")
        
        # Strength boost
        if "strength_boost" in effect:
            player.strength += effect["strength_boost"]
            messages.append(f"You feel stronger! +{effect['strength_boost']} strength!")
        
        # Consume one-time use items
        if found_item.item_type in ["potion", "treasure"]:
            self.game_state.inventory.pop(found_index)
            messages.append(f"(The {found_item.name} has been used up.)")
        
        # Publish event
        self.event_manager.publish(ITEM_USED, {
            "item": found_item.name,
            "effect": effect
        })
        
        return {
            "success": True,
            "message": "\n".join(messages),
            "data": {"item": found_item.name, "effect": effect}
        }
    
    def handle_inventory(self, args: list = None) -> dict:
        """Show player inventory."""
        inventory = self.game_state.inventory
        
        if not inventory:
            return {"success": True, "message": "Your inventory is empty."}
        
        items_list = []
        for item in inventory:
            items_list.append(f"  - {item.name}: {item.description} (Value: {item.value})")
        
        message = "=== Your Inventory ===\n\n" + "\n".join(items_list)
        
        return {
            "success": True,
            "message": message,
            "data": {"items": [item.name for item in inventory]}
        }
    
    def handle_stats(self, args: list = None) -> dict:
        """Show player statistics."""
        player = self.game_state.player
        
        message = f"""=== {player.name}'s Stats ===

Health: {player.health}/{player.max_health}
Mana: {player.mana}
Strength: {player.strength}
Level: {player.level}
Experience: {player.experience}

Location: {self.game_state.current_location.name}
Inventory: {len(self.game_state.inventory)} items
Visited: {len(self.game_state.visited_locations)} locations"""
        
        return {
            "success": True,
            "message": message,
            "data": {
                "health": player.health,
                "max_health": player.max_health,
                "mana": player.mana,
                "strength": player.strength,
                "level": player.level,
                "experience": player.experience
            }
        }
    
    def handle_attack(self, args: list) -> dict:
        """Handle combat - attack an enemy."""
        if not args:
            return {"success": False, "message": "Attack what? Specify an enemy."}
        
        target_name = " ".join(args).lower()
        location = self.game_state.current_location
        
        # Find enemy in location
        target_enemy = None
        for enemy in location.enemies:
            if target_name in enemy["name"].lower():
                target_enemy = enemy
                break
        
        if not target_enemy:
            return {"success": False, "message": f"There's no {target_name} here to attack."}
        
        # Combat!
        player = self.game_state.player
        
        # Player attacks
        damage_dealt = random.randint(player.strength - 2, player.strength + 3)
        target_enemy["health"] -= damage_dealt
        
        # Publish event
        self.event_manager.publish(ENEMY_DAMAGED, {
            "enemy": target_enemy["name"],
            "damage": damage_dealt
        })
        
        message = f"You attack the {target_enemy['name']} for {damage_dealt} damage!"
        
        # Check if enemy defeated
        if target_enemy["health"] <= 0:
            message += f"\n\n🎉 You defeated the {target_enemy['name']}!"
            
            # Remove enemy from location
            location.enemies.remove(target_enemy)
            
            # Award experience
            exp_gain = random.randint(15, 30)
            player.experience += exp_gain
            message += f"\nYou gain {exp_gain} experience!"
            
            # Check for level up
            new_level = (player.experience // 100) + 1
            if new_level > player.level:
                player.level = new_level
                player.max_health += 10
                player.health = player.max_health
                player.strength += 2
                message += f"\n\n🎊 LEVEL UP! You are now level {player.level}!"
                self.event_manager.publish(LEVEL_UP, {"level": new_level})
            
            self.event_manager.publish(ENEMY_DEFEATED, {
                "enemy": target_enemy["name"],
                "experience": exp_gain
            })
            
            if not location.enemies:
                message += "\n\nAll enemies defeated! The area is now safe."
                self.event_manager.publish(COMBAT_ENDED, {
                    "result": "victory",
                    "location": location.id
                })
        else:
            # Enemy counter-attacks
            enemy_damage = target_enemy.get("damage", 5)
            player.health -= enemy_damage
            message += f"\nThe {target_enemy['name']} attacks you for {enemy_damage} damage!"
            
            self.event_manager.publish(PLAYER_DAMAGED, {
                "damage": enemy_damage,
                "enemy": target_enemy["name"]
            })
            
            if player.health <= 0:
                message += "\n\n💀 You have been defeated! Game Over."
                self.game_state.game_status = "game_over"
        
        return {
            "success": True,
            "message": message,
            "data": {"enemy_health": target_enemy.get("health", 0)}
        }
    
    def handle_help(self, args: list = None) -> dict:
        """Show available commands."""
        if args:
            command = args[0].lower()
            help_text = self.parser.get_command_help(command)
            return {"success": True, "message": help_text}
        
        help_text = """=== Available Commands ===

Movement:
  move <direction> - Move in a direction (north, south, east, west)
  look - Look around the current location

Items:
  take <item> - Pick up an item
  drop <item> - Drop an item from inventory
  use <item> - Use an item (potions, etc.)
  inventory - Show your inventory

Combat:
  attack <enemy> - Attack an enemy

Information:
  stats - Show your character stats
  help - Show this help message

Game:
  save - Save your game
  load - Load a saved game

Examples:
  move north
  take sword
  use health potion
  attack goblin
  stats
"""
        return {"success": True, "message": help_text}
    
    def handle_save(self, args: list = None) -> dict:
        """Save the game."""
        return {"success": True, "message": "Game saved! (Demo - not persisted to disk)"}
    
    def handle_load(self, args: list = None) -> dict:
        """Load a saved game."""
        return {"success": True, "message": "No saved games found. Start a new game!"}


# Global game engine instance
game_engine = GameEngine()
