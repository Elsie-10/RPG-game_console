# Game Routes
# API endpoints for game state, navigation, and actions

from flask import Blueprint, jsonify, request
from game_engine.engine import GameEngine, game_engine
from Repositories.game_state_repository import GameStateRepository

# Create blueprint
game_bp = Blueprint('game', __name__)

# Global game engine instance (shared with command routes)
game_state_repo = GameStateRepository()

@game_bp.route('/game/start', methods=['POST'])
def start_game():
    """Start a new game."""
    # Initialize the game world
    game_engine.initialize_world()
    
    # Initialize game state repository
    game_state_repo.initialize_new_game()
    
    return jsonify({
        "success": True,
        "message": "Game started!",
        "data": {
            "location": game_engine.game_state.current_location.name,
            "player": {
                "name": game_engine.game_state.player.name,
                "health": game_engine.game_state.player.health,
                "level": game_engine.game_state.player.level
            }
        }
    })

@game_bp.route('/game/state', methods=['GET'])
def get_game_state():
    """Get current game state."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress. Start a game first."
        }), 400
    
    state = game_engine.game_state
    
    return jsonify({
        "success": True,
        "data": {
            "player": {
                "name": state.player.name,
                "health": state.player.health,
                "max_health": state.player.max_health,
                "mana": state.player.mana,
                "strength": state.player.strength,
                "level": state.player.level,
                "experience": state.player.experience
            },
            "location": {
                "id": state.current_location.entity_id,
                "name": state.current_location.name,
                "description": state.current_location.description,
                "exits": list(state.current_location.exits.keys()),
                "items": state.current_location.items,
                "enemies": state.current_location.enemies
            },
            "inventory": [item.name for item in state.inventory],
            "game_status": state.game_status,
            "visited_locations": list(state.visited_locations)
        }
    })

@game_bp.route('/game/location', methods=['GET'])
def get_current_location():
    """Get current location details."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    location = game_engine.game_state.current_location
    
    # Get item details
    items = []
    for item_id in location.items:
        if item_id in game_engine.items_db:
            item = game_engine.items_db[item_id]
            items.append({
                "id": item.entity_id,
                "name": item.name,
                "description": item.description,
                "type": item.item_type
            })
    
    return jsonify({
        "success": True,
        "data": {
            "id": location.entity_id,
            "name": location.name,
            "description": location.description,
            "exits": location.exits,
            "items": items,
            "enemies": location.enemies
        }
    })

@game_bp.route('/game/location/<direction>', methods=['POST'])
def move_player(direction):
    """Move player in a direction."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    result = game_engine.handle_move([direction])
    
    if result.get("success"):
        # Update game state repository
        game_state_repo.update_location(
            game_engine.game_state.current_location.entity_id
        )
    
    return jsonify(result)

@game_bp.route('/game/look', methods=['GET'])
def look_around():
    """Look around the current location."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    result = game_engine.handle_look()
    return jsonify(result)

@game_bp.route('/game/inventory', methods=['GET'])
def get_inventory():
    """Get player inventory."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    result = game_engine.handle_inventory()
    return jsonify(result)

@game_bp.route('/game/stats', methods=['GET'])
def get_stats():
    """Get player stats."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    result = game_engine.handle_stats()
    return jsonify(result)

# New action processing endpoints
@game_bp.route('/game/take/<item_name>', methods=['POST'])
def take_item(item_name):
    """Take an item from the current location."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    result = game_engine.handle_take([item_name])
    return jsonify(result)

@game_bp.route('/game/drop/<item_name>', methods=['POST'])
def drop_item(item_name):
    """Drop an item from inventory."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    result = game_engine.handle_drop([item_name])
    return jsonify(result)

@game_bp.route('/game/attack/<enemy_name>', methods=['POST'])
def attack_enemy(enemy_name):
    """Attack an enemy in the current location."""
    if not game_engine.game_state:
        return jsonify({
            "success": False,
            "message": "No game in progress."
        }), 400
    
    result = game_engine.handle_attack([enemy_name])
    return jsonify(result)