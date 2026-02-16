# Event Manager
# Handles game events and event-driven communication

from typing import Callable, Dict, List
from dataclasses import dataclass
from datetime import datetime

# Event Type Constants
# These define all possible events in our game
# Using constants prevents typos and makes it easy to find all event types
PLAYER_MOVED = "player_moved"
ITEM_PICKED_UP = "item_picked_up"
ITEM_DROPPED = "item_dropped"
ITEM_USED = "item_used"
COMBAT_STARTED = "combat_started"
COMBAT_ENDED = "combat_ended"
PLAYER_DAMAGED = "player_damaged"
PLAYER_HEALED = "player_healed"
ENEMY_DEFEATED = "enemy_defeated"
ENEMY_DAMAGED = "enemy_damaged"
GAME_STARTED = "game_started"
GAME_SAVED = "game_saved"
GAME_LOADED = "game_loaded"
LEVEL_UP = "level_up"
INVENTORY_UPDATED = "inventory_updated"


@dataclass
class GameEvent:
    """
    GameEvent represents something that happened in the game.
    
    Attributes:
        type: The type of event (e.g., "player_moved")
        data: Dictionary containing event-specific data
        timestamp: When the event occurred
    """
    type: str
    data: dict
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()


class EventManager:
    """
    EventManager handles event-driven communication in the game.
    
    How it works:
    1. Other parts of the code SUBSCRIBE to specific event types
    2. When something happens, code PUBLISHES an event
    3. EventManager notifies all subscribed functions (callbacks)
    
    Why use events?
    - Decoupling: Game components don't need to know about each other
    - Flexibility: Easy to add new listeners without changing existing code
    - Logging: Easy to track what happens in the game
    - UI Updates: UI can listen to events to update the display
    
    Example usage:
        def on_player_move(event):
            print(f"Player moved to {event.data['location']}")
        
        event_manager.subscribe(PLAYER_MOVED, on_player_move)
        event_manager.publish(PLAYER_MOVED, {"location": "forest"})
    """
    
    def __init__(self):
        # Dictionary to store event type -> list of callbacks
        # Example: {"player_moved": [callback1, callback2]}
        self._events: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable) -> bool:
        """
        Subscribe to an event type.
        
        Args:
            event_type: The type of event to listen for
            callback: Function to call when event is published
            
        Returns:
            True if subscribed successfully
        """
        if event_type not in self._events:
            self._events[event_type] = []
        
        # Don't add duplicate callbacks
        if callback not in self._events[event_type]:
            self._events[event_type].append(callback)
            return True
        return False
    
    def unsubscribe(self, event_type: str, callback: Callable) -> bool:
        """
        Unsubscribe from an event type.
        
        Args:
            event_type: The type of event to stop listening for
            callback: The callback function to remove
            
        Returns:
            True if unsubscribed successfully
        """
        if event_type in self._events:
            if callback in self._events[event_type]:
                self._events[event_type].remove(callback)
                return True
        return False
    
    def publish(self, event_type: str, data: dict = None) -> GameEvent:
        """
        Publish an event to all subscribers.
        
        Args:
            event_type: The type of event to publish
            data: Dictionary of event data
            
        Returns:
            The created GameEvent object
        """
        # Create the event with data (default to empty dict)
        if data is None:
            data = {}
        
        event = GameEvent(type=event_type, data=data)
        
        # Notify all subscribers
        if event_type in self._events:
            for callback in self._events[event_type]:
                try:
                    callback(event)
                except Exception as e:
                    # Log error but don't stop processing other callbacks
                    print(f"Error in event callback: {e}")
        
        return event
    
    def clear_subscribers(self, event_type: str = None):
        """
        Clear subscribers for a specific event or all events.
        
        Args:
            event_type: If provided, clear only this event type.
                       If None, clear all events.
        """
        if event_type:
            if event_type in self._events:
                self._events[event_type] = []
        else:
            self._events.clear()
    
    def get_subscriber_count(self, event_type: str) -> int:
        """
        Get the number of subscribers for an event type.
        
        Args:
            event_type: The event type to check
            
        Returns:
            Number of subscribers
        """
        return len(self._events.get(event_type, []))


# Global event manager instance
# This allows easy importing throughout the game
event_manager = EventManager()

