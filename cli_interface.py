import requests
import json

BASE_URL = 'http://127.0.0.1:5000/api'  # Adjust if your API is on a different port/host

def print_response(response):
    """Helper to print API responses."""
    if response.status_code == 200:
        data = response.json()
        print("Success:", json.dumps(data, indent=2))
    else:
        print("Error:", response.status_code, response.text)

def main():
    print("Welcome to the RPG Fantasy Game CLI!")
    print("Type 'start' to begin, 'quit' to exit, or enter commands (e.g., 'look', 'go north').")
    
    while True:
        user_input = input("> ").strip().lower()
        if user_input == 'quit':
            print("Goodbye!")
            break
        elif user_input == 'start':
            response = requests.post(f"{BASE_URL}/game/start")
            print_response(response)
        else:
            # Send as a general command
            response = requests.post(f"{BASE_URL}/command", json={"command": user_input})
            print_response(response)

if __name__ == '__main__':
    main()