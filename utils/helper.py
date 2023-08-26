""" 
Created on : 26/08/23 11:27 am
@author : ds  
"""
import json,uuid

def load_list():
    try:
        with open('/Users/ds/PycharmProjects/Microservices/data/todo.json', 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


def save_list(todo_list):
    try:
        with open('/Users/ds/PycharmProjects/Microservices/data/todo.json', 'w') as file:
            json.dump(todo_list, file)
    except Exception as e:
        print(f"An error occurred: {e}")


def generate_id():
    return uuid.uuid4().hex

