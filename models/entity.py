# entity is the parent class for all game object(chatacter,item,location)
class Entity:
    def __init__(self,id,name,description):
        self.entity_id = id
        self.name = name
        self.description = description
# all game objects should have properties like name and description