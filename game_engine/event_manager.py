from typing import Callable,Dict,List
from dataclasses import dataclass
from datetime import datetime

@dataclass 
class GameEvent:
    type: str #(e.g, "Player_moved")
    data: dict #(e.g, {"location": "forest"})
    timestamp: datetime = None # Optional, auto-set when created
class EventManager:
    def __init__(self):
        self._events:Dict[str,List[Callable]] = {}

    def subscribe(self,event_type:str, callback: Callable ):
        #sign up for notification
        pass
    
    def publish(self, event_type:str, data: dict):
        #send notification
        pass
        