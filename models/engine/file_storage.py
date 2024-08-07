#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
<<<<<<< HEAD
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
=======
    """
    Handles long term storage of all class instances
    """
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
        """
        Returns private attribute: __objects
        """
>>>>>>> 9680e81 (pushed)
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
<<<<<<< HEAD
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
=======
        """
        Sets / updates in __objects the obj with key <obj class name>.id
        """
        bm_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[bm_id] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        fname = FileStorage.__file_path
        storage_d = {}
        for bm_id, bm_obj in FileStorage.__objects.items():
            storage_d[bm_id] = bm_obj.to_json(saving_file_storage=True)
        try:
            with open(fname, mode='w', encoding='utf-8') as f_io:
                json.dump(storage_d, f_io)
        except Exception as e:
            print(f"An error occurred while saving: {e}")

    def reload(self):
        """
        If file exists, deserializes JSON file to __objects, else nothing
        """
        fname = FileStorage.__file_path
        FileStorage.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
            for o_id, d in new_objs.items():
                k_cls = d['__class__']
                FileStorage.__objects[o_id] = FileStorage.CNC[k_cls](**d)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"An error occurred while reloading: {e}")

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it's inside
        """
        if obj:
            obj_ref = "{}.{}".format(type(obj).__name__, obj.id)
            all_class_objs = self.all(obj.__class__.__name__)
            if all_class_objs.get(obj_ref):
                del FileStorage.__objects[obj_ref]
            self.save()

    def delete_all(self):
        """
        Deletes all stored objects, for testing purposes
        """
        try:
            with open(FileStorage.__file_path, mode='w'):
                pass
        except Exception as e:
            print(f"An error occurred while deleting all: {e}")
        del FileStorage.__objects
        FileStorage.__objects = {}
        self.save()

    def close(self):
        """
        Calls the reload() method for deserialization from JSON to objects
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieves one object based on class name and id
        """
        if cls and id:
            fetch_obj = "{}.{}".format(cls, id)
            all_obj = self.all(cls)
            return all_obj.get(fetch_obj)
        return None

    def count(self, cls=None):
        """
        Count of all objects in storage
        """
        return len(self.all(cls))
>>>>>>> 9680e81 (pushed)
