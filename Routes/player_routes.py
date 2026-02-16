# Player Routes
# API endpoints for player creation, updates, stats, and character management

from flask import Blueprint, jsonify, request
from game_engine.engine import game_engine

# Create blueprint
player_bp = Blueprint('player', __name__)

@player_bp.route('/player', methods=['POST'])
def create_player():
    """Create a new player."""
    data = request.get_json()
    name = data.get('name')
    if not name:
        return jsonify({"success": False, "message": "Player name is required."}), 400
    
    # Assuming game_engine has a create_player method
    result = game_engine.create_player(name)
    return jsonify(result)

@player_bp.route('/player', methods=['PUT'])
def update_player():
    """Update player attributes (e.g., name, stats)."""
    if not game_engine.game_state:
        return jsonify({"success": False, "message": "No game in progress."}), 400
    
    data = request.get_json()
    updates = {}
    if 'name' in data:
        updates['name'] = data['name']
    if 'health' in data:
        updates['health'] = data['health']
    # Add more fields as needed (e.g., mana, strength)
    
    # Assuming game_engine has an update_player method
    result = game_engine.update_player(updates)
    return jsonify(result)

@player_bp.route('/player/stats', methods=['GET'])
def view_player_stats():
    """View player stats."""
    if not game_engine.game_state:
        return jsonify({"success": False, "message": "No game in progress."}), 400
    
    player = game_engine.game_state.player
    return jsonify({
        "success": True,
        "data": {
            "name": player.name,
            "health": player.health,
            "max_health": player.max_health,
            "mana": player.mana,
            "strength": player.strength,
            "level": player.level,
            "experience": player.experience
        }
    })

@player_bp.route('/player/equip/<item_name>', methods=['POST'])
def equip_item(item_name):
    """Equip an item from inventory (character management)."""
    if not game_engine.game_state:
        return jsonify({"success": False, "message": "No game in progress."}), 400
    
    # Assuming game_engine has a handle_equip method
    result = game_engine.handle_equip([item_name])
    return jsonify(result)
