# Game Console Development Plan

## Learning Goals
Build a Fantasy RPG game with:
- Flask web interface + CLI interface
- Character management system
- Inventory system
- Location/world navigation
- Clean, modular architecture

## Phase 1: Foundation (Week 1-2)
### 1.1 Project Structure & Configuration
- [ ] Set up app.py with Flask application factory pattern
- [ ] Create config.py with development/production configs
- [ ] Set up requirements.txt

### 1.2 Core Models
- [ ] Create base entity model (Entity class)
- [ ] Create Character model (player)
- [ ] Create Item model (inventory items)
- [ ] Create Location model (world navigation)

### 1.3 Repository Layer (Data Management)
- [ ] Create base repository pattern
- [ ] Implement player repository
- [ ] Implement game state repository

## Phase 2: Game Engine (Week 2-3)

### 2.1 Event System (event_manager.py)
**Guidelines:**
- [ ] Create `EventManager` class with `_events = {}` dictionary to store event listeners
- [ ] Implement `subscribe(event_type: str, callback: callable)` - Add callback to event's listener list
- [ ] Implement `unsubscribe(event_type: str, callback: callable)` - Remove callback from listeners
- [ ] Implement `publish(event_type: str, data: dict)` - Loop through callbacks and call them with data
- [ ] Define event type constants at module level: `PLAYER_MOVED`, `ITEM_PICKED_UP`, `ITEM_DROPPED`, `COMBAT_STARTED`, `COMBAT_ENDED`, `PLAYER_DAMAGED`, `ENEMY_DEFEATED`
- [ ] Create `Event` dataclass or namedtuple with: `type`, `data`, `timestamp`

**Code Structure:**
```python
# event_manager.py
from typing import Callable, Dict, List
# List[str] = a list containing strings
#Dict[str, int] = a dictionary with string key and int values
# callable[[int,str], bool]= a function that takes (int,str) and return bool
from dataclasses import dataclass
from datetime import datetime

# Event Types (constants)
PLAYER_MOVED = "player_moved"
ITEM_PICKED_UP = "item_picked_up"
# ... more events

@dataclass
class GameEvent:
    type: str
    data: dict
    timestamp: datetime = None

class EventManager:
    def __init__(self):
        self._events: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        # Get or create list, append callback
        pass
    
    def publish(self, event_type: str, data: dict):
        # Create event, call all callbacks
        pass
```

---

### 2.2 Command Parser (command_parser.py)
**Guidelines:**
- [ ] Create `CommandParser` class with a dictionary of known commands
- [ ] Implement `parse(input_string: str)` method that:
  - Strips whitespace and converts to lowercase
  - Splits into words using `split()` 
  - First word = command, remaining = arguments
  - Returns `ParsedCommand` namedtuple/dict with: `command`, `args`, `raw`
- [ ] Supported commands to implement:
  - `move [direction]` - Navigate to adjacent location
  - `look` - Describe current location
  - `take [item_name]` - Pick up an item
  - `drop [item_name]` - Drop an item from inventory
  - `use [item_name]` - Use an item
  - `inventory` or `i` - Show player inventory
  - `stats` or `s` - Show player statistics
  - `attack [target]` - Attack an enemy
  - `help` - Show available commands
- [ ] Add validation - return error if command not recognized

**Code Structure:**
```python
# command_parser.py
from typing import NamedTuple

class ParsedCommand(NamedTuple):
    command: str
    args: list
    raw: str

class CommandParser:
    COMMANDS = {
        'move': ['direction'],
        'look': [],
        'take': ['item_name'],
        # ... more commands
    }
    
    def parse(self, input_string: str) -> ParsedCommand:
        # Clean input: strip(), lower()
        # Split into parts
        # Validate command exists
        # Return ParsedCommand
        pass
```

---

### 2.3 Game Engine (engine.py)
**Guidelines:**
- [ ] Create `GameState` class to hold:
  - `player: Character`
  - `current_location: Location`
  - `inventory: List[Item]`
  - `game_status: str` (e.g., 'playing', 'combat', 'game_over')
  - `visited_locations: Set[str]`
- [ ] Create `GameEngine` class with:
  - `event_manager: EventManager` instance
  - `game_state: GameState`
  - `world: Dict[str, Location]` - All locations by ID
- [ ] Implement `initialize_world()`:
  - Create 3-5 connected locations (start, forest, village, dungeon, treasure_room)
  - Add items to locations
  - Add enemies to some locations
  - Set up exits between locations
  - Set player starting location
- [ ] Implement `process_command(command: ParsedCommand) -> dict`:
  - Route to appropriate handler based on command
  - Return `{"success": bool, "message": str, "data": dict}`
- [ ] Implement command handlers:
  - `handle_move(args)` - Check exits, update location, publish event
  - `handle_look()` - Return location description, items, enemies, exits
  - `handle_take(args)` - Move item from location to inventory
  - `handle_drop(args)` - Move item from inventory to location
  - `handle_use(args)` - Apply item effects (health potions, etc.)
  - `handle_inventory()` - List player inventory
  - `handle_stats()` - Return player stats
  - `handle_attack(args)` - Combat logic
- [ ] Integrate with EventManager - publish events after state changes

**Code Structure:**
```python
# engine.py
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
```

---

### Phase 2 Success Criteria:
- [ ] Event system allows subscribing/publishing game events
- [ ] Command parser correctly parses user input into structured commands
- [ ] Game engine processes commands and updates game state
- [ ] World has at least 4 connected locations
- [ ] Basic navigation, look, inventory, and stats commands work
- [ ] Events are published when player moves or picks up items

## Phase 3: API Routes (Week 3-4)
### 3.1 Player Routes
- [ ] Create/update player
- [ ] View player stats
- [ ] Character management

### 3.2 Game Routes
- [ ] Navigation commands
- [ ] Game state queries
- [ ] Action processing

### 3.3 Command Routes
- [ ] Process game commands
- [ ] Return game responses

## Phase 4: Interfaces (Week 4-5)
### 4.1 Web Interface
- [ ] Create HTML templates
- [ ] Terminal-style CSS
- [ ] JavaScript for API calls

### 4.2 CLI Interface
- [ ] Command line interface
- [ ] Interactive game loop
- [ ] Color output (optional)

## Phase 5: Polish & Expand (Week 5+)
### 5.1 Features
- [ ] Combat system
- [ ] Quest system
- [ ] Save/Load functionality
- [ ] More items and locations

### 5.2 Documentation
- [ ] README with usage guide
- [ ] Code comments
- [ ] Architecture documentation

## Learning Notes
Each phase includes:
- Concept explanations
- Why we structure code this way
- Best practices
- Hands-on implementation

## Time Expectation
- Phase 1-2: 2-3 weeks (learning fundamentals)
- Phase 3-4: 2-3 weeks (building features)
- Phase 5+: Ongoing (enhancements)

## Success Criteria
- [ ] Game runs in both web and CLI
- [ ] Can create characters and manage inventory
- [ ] Can navigate through locations
- [ ] Clean, maintainable code
- [ ] You understand the architecture

