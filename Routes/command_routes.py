# Command Routes
# API endpoints for processing general game commands and returning responses

from flask import Blueprint, jsonify, request
from game_engine.engine import game_engine

# Create blueprint
command_bp = Blueprint('command', __name__)

@command_bp.route('/command', methods=['POST'])
def process_command():
    """Process a general game command and return the response."""
    if not game_engine.game_state:
        return jsonify({"success": False, "message": "No game in progress."}), 400
    
    data = request.get_json()
    command = data.get('command')
    if not command:
        return jsonify({"success": False, "message": "Command is required."}), 400
    
    # Assuming game_engine has a process_command method that takes a list of words
    result = game_engine.process_command(command.split())
    return jsonify(result)