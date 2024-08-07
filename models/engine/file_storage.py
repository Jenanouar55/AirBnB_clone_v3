#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""
from cgi import FieldStorage
import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """handles long term storage of all class instances"""
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    """CNC - this variable is a dictionary with:
    keys: Class Names
    values: Class type (used for instantiation)
    """
    __file_path = './dev/file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns all objects or objects of a specific class"""
        if cls:
            objects_dict = {}
        for class_id, obj in FileStorage.__objects.items():
            if type(obj).__name__ == cls.__name__:
                objects_dict[class_id] = obj
        return objects_dict
        return FileStorage.__objects

    def new(self, obj):
        """Sets/updates in __objects the obj with key <obj class name>.id"""
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """Serializes __objects to the JSON file (path: __file_path)"""
        fname = FileStorage.__file_path
        d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            d[bm_id] = bm_obj.to_json()
        try:
            with open(fname, mode='w', encoding='utf-8') as f_io:
                json.dump(d, f_io)
        except IOError as e:
            print(f"Error writing to file {fname}: {e}")

    def reload(self):
        """If file exists, deserializes JSON file to __objects; else nothing"""
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
    try:
        with open(fname, mode='r', encoding='utf-8') as f_io:
            new_objs = json.load(f_io)
    except FileNotFoundError:
        return
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from file {fname}: {e}")
        return
    except IOError as e:
        print(f"Error reading file {fname}: {e}")
        return
    for o_id, d in new_objs.items():
        k_cls = d['__class__']
        FieldStorage.__objects[o_id] = FieldStorage.CNC[k_cls](**d)

    def delete(self, obj=None):
        """Deletes obj from __objects if it's inside"""
        if obj is None:
            return
        obj_id = "{}.{}".format(type(obj).__name__, obj.id)
        if obj_id in FileStorage.__objects:
            del FileStorage.__objects[obj_id]
        else:
            print(f"Object {obj_id} not found in __objects.")

    def close(self):
        """
            calls the reload() method for deserialization from JSON to objects
        """
        self.reload()

    def get(self, cls, id):
        """Retrieve one object"""
        if cls.__name__ in self.all():
            return self.all()[cls.__name__].get(id)
        return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            return len(self.__objects.get(cls.__name__, {}))
        count = 0
        for obj_dict in self.__objects.values():
            count += len(obj_dict)
        return count
