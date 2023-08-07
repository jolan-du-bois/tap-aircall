import json
import os

def process_state_file():
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, "state.json")

        # Read the content of the state.json file
        with open(file_path, 'r') as infile:
            data = json.load(infile)

        # Extract the "value" field from the JSON data
        new_data = data.get("value", {})

        # Update the state.json file with the new JSON object
        with open(file_path, 'w') as outfile:
            json.dump(new_data, outfile)

        print("state.json has been updated successfully.")
    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except json.JSONDecodeError:
        print(f"Invalid JSON format in {file_path}.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    process_state_file()
