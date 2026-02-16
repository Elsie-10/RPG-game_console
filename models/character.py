# A player or NPC in the game
from models.entity import Entity 

class Character(Entity):
    max_health = 100 # class variable

    def __init__(self,id,name,description,health,mana,strength,level,experience):
        super().__init__(id,name, description)
        self.health = health # Instance variable
        self.mana = mana
        self.strength = strength
        self.level = level
        self.experience = experience
    