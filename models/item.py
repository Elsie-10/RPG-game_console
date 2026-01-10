# something the player can pick up, use, or equip
class Item(Entity):
    def __init__(self,id,name,description,item_type,value,effect,can_equip):
        super().__init__(id,name,description)
        self.item_type = item_type
        self.value = value
        self.effect = effect
        self.can_equip = can_equip

# Pre-defined items
WEAPONS = {
    "iron_sword": {"name": "Iron Sword", "value": 10, "effect": "+5 attack"},
    "magic_staff": {"name": "Magic Staff", "value": 50, "effect": "+20 magic"}
}
POTIONS = {
    "health_potion": {"name": "Health Potion", ...},
    "mana_potion": {"name": "Mana Potion", ...}
}

# Create item by name
def create_item(item_id, item_type, name):
    data = WEAPONS.get(item_type, {}) # <- looks up in dictionary
    data = POTIONS.get(item_type, {})
    return Item(item_id, name, data.get("description", ""), item_type, 
                data.get("value", 0), data.get("effect", ""), True)
