# A place in the game world(room,forest,city)
class Location(Entity):
    def __init__(self,id ,name, description,exits, items,enemies,is_locked):
        super().__init__(id,name,description)
        self.exits = exits
        self.items = items
        self.enemies = enemies 
        self.is_locked = is_locked