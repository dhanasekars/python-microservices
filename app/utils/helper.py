""" 
Created on : 26/08/23 11:27 am
@author : ds  
"""
import json
import uuid
import logging
from fastapi import HTTPException

from app.utils.config_manager import config_manager

config_manager.configure_logging()


def load_list():
    """Load json to an object"""
    try:
        with open(
            config_manager.config_data.get("data_file"),
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)
            logging.info(
                f"Loaded data successfully from {config_manager.config_data.get('data_file')}"
            )
            return data
    except FileNotFoundError:
        logging.info("Data file not found. Returning an empty list.")
        return []
    except ValueError as err:
        logging.error(f"Error loading data. Value Error: {str(err)}")
        return err


def get_todo_details(todo_id):
    """to get the details for a given id"""
    logging.info(f"Fetching todo details for ID: {todo_id}")

    data = load_list()

    if not isinstance(data, list):
        error_message = "Invalid data format. Expected a list."
        logging.error(error_message)
        return {"error": error_message}

    if len(data) == 0:
        warning_message = "No data in the system."
        logging.warning(warning_message)
        return {"error": warning_message}

    for item in data:
        if item["id"] == todo_id:
            logging.debug(f"Found todo details for ID {todo_id}: {item}")
            return item

    error_message = f"Todo not found for the given ID: {todo_id}"
    logging.warning(error_message)
    raise HTTPException(status_code=404, detail=error_message)


def save_list(todo_list):
    """save object to json file"""
    try:
        file_path = config_manager.config_data.get("data_file")
        logging.debug(f"Saving data to file: {file_path}")

        with open(
            file_path,
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(todo_list, file)
            logging.debug("Data saved successfully.")
            return True

    except FileNotFoundError:
        error_message = "File not found. Check the file path."
        logging.error(error_message)
        return error_message

    except PermissionError:
        error_message = "Permission denied. Check file permissions."
        logging.error(error_message)
        return error_message

    except json.JSONDecodeError:
        error_message = "Error encoding data to JSON."
        logging.error(error_message)
        return error_message

    except Exception as err:
        error_message = f"An unexpected error occurred: {str(err)}"
        logging.error(error_message)
        return error_message


def remove_todo(todo_id):
    """function to remove an item from the list"""
    logging.debug(f"Removing item with ID: {todo_id}")

    data = load_list()
    # New list with item for the given id removed
    updated_data = [item for item in data if item["id"] != todo_id]

    if len(data) == len(updated_data):
        error_message = "ID not found"
        logging.warning(error_message)
        raise HTTPException(status_code=404, detail=error_message)
    save_list(updated_data)
    success_message = f"Item with ID {todo_id} removed"
    logging.info(success_message)
    raise HTTPException(status_code=200, detail=success_message)


def update_todo(todo_id, todo):
    """function to update an item."""
    logging.debug(f"Updating item with ID: {todo_id}")

    data = load_list()
    updated = False

    for item in data:
        if item["id"] == todo_id:
            logging.debug(f"Found item with ID {todo_id} for update.")
            for key, value in todo.items():
                if value is not None and key in item:
                    logging.debug(f"Updating {key} to {value}.")
                    item[key] = value
            updated = True
            break
    if not updated:
        error_message = f"{todo_id} not found."
        logging.warning(error_message)
        raise HTTPException(status_code=404, detail=error_message)

    save_list(data)
    success_message = f"{todo_id} updated successfully."
    logging.info(success_message)
    return {"success": success_message}


def generate_id():
    """generate a UUID for each task"""
    new_id = uuid.uuid4().hex
    logging.debug(f"Generated new ID: {new_id}")
    return new_id
