""" 
Created on : 26/08/23 11:27 am
@author : ds  
"""
import json
import uuid
from config.config_manager import config_manager


def load_list():
    """Load json to an object"""
    try:
        with open(
            config_manager.config_data.get("data_file"),
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []
    except ValueError as e:
        return e


def get_todo_details(todo_id):
    """to get the details for a given id"""
    data = load_list()

    if not isinstance(data, list):
        return {"error": "Invalid data format. Expected a list."}

    if len(data) == 0:
        return {"error": "No data in the system."}

    for item in data:
        if item["id"] == todo_id:
            return item

    return {"error": "Todo not found for the given id."}


def save_list(todo_list):
    """save object to json file"""
    try:
        with open(
            config_manager.config_data.get("data_file"),
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(todo_list, file)
            return True
    except FileNotFoundError:
        return "File not found. Check the file path."
    except PermissionError:
        return "Permission denied. Check file permissions."
    except json.JSONDecodeError:
        return "Error encoding data to JSON."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"


def remove_todo(todo_id):
    """function to remove an item from the list"""
    data = load_list()
    # New list with item for the given id removed
    updated_data = [item for item in data if item["id"] != todo_id]

    if len(data) == len(updated_data):
        return {"error": "Id not found"}

    save_list(updated_data)
    return {"success": f"{todo_id} removed"}


def update_todo(todo_id, todo):
    """function to update an item."""
    data = load_list()
    updated = False

    for item in data:
        if item["id"] == todo_id:
            for key, value in todo.items():
                if value is not None and key in item:
                    item[key] = value
            updated = True
            break
    if not updated:
        return {"error": f"{todo_id} not found."}

    save_list(data)
    return {"success": f"{todo_id} updated successfully."}


def generate_id():
    """generate a UUID for each task"""
    return uuid.uuid4().hex
