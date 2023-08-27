""" 
Created on : 26/08/23 11:27 am
@author : ds  
"""
import json
import uuid


def load_list():
    """ Load json to an object"""
    try:
        with open(
            "/Users/ds/PycharmProjects/Microservices/data/todo.json", "r", encoding='utf-8'
        ) as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        return e
    except Exception as e:
        return e

def get_todo_details(todo_id):
    data = load_list()
    for item in data:
        if item["id"] == todo_id:
            return item
    return None

def remove_todo(todo_id):
    data = load_list()
    initial_length = len(data)
    for item in data:
        if item["id"] == todo_id:
            data.remove(item)
            break
    new_length = len(data)
    if initial_length == new_length:
        return None
    else:
        return data

def save_list(todo_list):
    """ save object to json file"""
    try:
        with open(
            "/Users/ds/PycharmProjects/Microservices/data/todo.json", "w", encoding='utf-8'
        ) as file:
            json.dump(todo_list, file)
            return { "success"}
    except Exception as e:
        return e


def generate_id():
    """generate a UUID for each task"""
    return uuid.uuid4().hex

