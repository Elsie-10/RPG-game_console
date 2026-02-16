# Base Repository Pattern
# This is the foundation for all data access in our game
# Provides common CRUD (Create, Read, Update, Delete) operations

from typing import TypeVar, Generic, List, Optional
from dataclasses import dataclass, field

# Type variable for generic repository
T = TypeVar('T')

@dataclass
class BaseRepository(Generic[T]):
    """
    BaseRepository provides a template for data storage operations.
    
    In our RPG game, we'll have:
    - PlayerRepository: manages player characters
    - GameStateRepository: manages saved games
    - ItemRepository: manages game items (optional)
    
    Why use a repository pattern?
    - Separates data access logic from business logic
    - Makes it easy to change data storage (file, database, memory)
    - Provides consistent interface for all data operations
    """
    
    # In-memory storage - in a real app, this could be a database
    _storage: dict = field(default_factory=dict)
    
    def create(self, id: str, entity: T) -> T:
        """
        Create a new entity in storage.
        
        Args:
            id: Unique identifier for the entity
            entity: The entity object to store
            
        Returns:
            The created entity
        """
        self._storage[id] = entity
        return entity
    
    def get(self, id: str) -> Optional[T]:
        """
        Retrieve an entity by its ID.
        
        Args:
            id: The unique identifier
            
        Returns:
            The entity if found, None otherwise
        """
        return self._storage.get(id)
    
    def get_all(self) -> List[T]:
        """
        Get all entities in storage.
        
        Returns:
            List of all stored entities
        """
        return list(self._storage.values())
    
    def update(self, id: str, entity: T) -> Optional[T]:
        """
        Update an existing entity.
        
        Args:
            id: The unique identifier
            entity: The updated entity
            
        Returns:
            The updated entity if found, None otherwise
        """
        if id in self._storage:
            self._storage[id] = entity
            return entity
        return None
    
    def delete(self, id: str) -> bool:
        """
        Delete an entity by its ID.
        
        Args:
            id: The unique identifier
            
        Returns:
            True if deleted, False if not found
        """
        if id in self._storage:
            del self._storage[id]
            return True
        return False
    
    def exists(self, id: str) -> bool:
        """
        Check if an entity exists.
        
        Args:
            id: The unique identifier
            
        Returns:
            True if exists, False otherwise
        """
        return id in self._storage
    
    def clear(self):
        """Clear all entities from storage."""
        self._storage.clear()

