#!/usr/bin/python3
"""
Command interpreter for AirBnB project
"""
import os
import cmd
import json
from models import base_model, user, storage, CNC

BaseModel = base_model.BaseModel
User = user.User


class HBNBCommand(cmd.Cmd):
    """
        Command interpreter class
    """
    prompt = '(hbnb) '
    ERR = [
        '** class name missing **',
        '** class doesn\'t exist **',
        '** instance id missing **',
        '** no instance found **',
        '** attribute name missing **',
        '** value missing **',
    ]

    def preloop(self):
        """
            handles intro to command interpreter
        """
        print(r'.----------------------------.')
        print(r'|    Welcome to hbnb CLI!    |')
        print(r'|   for help, input \'help\'   |')
        print(r'|   for quit, input \'quit\'   |')
        print(r'.----------------------------.')

    def postloop(self):
        """
            handles exit to command interpreter
        """
        print(r'.----------------------------.')
        print(r'|  Well, that sure was fun!  |')
        print(r'.----------------------------.')

    def default(self, line):
        """
            default response for unknown commands
        """
        pass

    def emptyline(self):
        """
            Called when an empty line is entered in response to the prompt.
        """
        pass

    def __class_err(self, arg):
        """
            private: checks for missing class or unknown class
        """
        error = 0
        if len(arg) == 0:
            print(HBNBCommand.ERR[0])
            error = 1
        else:
            if isinstance(arg, list):
                arg = arg[0]
            if arg not in CNC.keys():
                print(HBNBCommand.ERR[1])
                error = 1
        return error

    def __id_err(self, arg):
        """
            private checks for missing ID or unknown ID
        """
        error = 0
        if len(arg) < 2:
            error += 1
            print(HBNBCommand.ERR[2])
        if not error:
            file_storage_objs = storage.all()
            for key, value in file_storage_objs.items():
                temp_id = key.split('.')[1]
                if temp_id == arg[1] and arg[0] in key:
                    return error
            error += 1
            print(HBNBCommand.ERR[3])
        return error

    def do_airbnb(self, arg):
        """airbnb: airbnb
        SYNOPSIS: Command changes prompt string"""
        print("                      __ ___                        ")
        print("    _     _  _ _||\\ |/  \\ | _  _  _|_|_     _  _ _| ")
        print(" |_||_))/(_|| (_|| \\|\\__/ || )(_)| |_| ))/(_|| (_| ")
        print("   |                                                ")
        if HBNBCommand.prompt == '(hbnb) ':
            HBNBCommand.prompt = " /_ /_ _  /_\\n/ //_// //_/ "
        else:
            HBNBCommand.prompt = '(hbnb) '
        arg = arg.split()
        error = self.__class_err(arg)

    def do_quit(self, line):
        """quit: quit
        USAGE: Command to quit the program
        """
        return True

    def do_EOF(self, line):
        """function to handle EOF"""
        print()
        return True

    def __parse_string(self, value):
        """ parses attribute value passed as string """
        value = value.strip('"').replace('_', ' ')
        index = 0
        while index < len(value):
            index = value.find('\\', index)
            if index == -1:
                break
            if value[index + 1] == '"':
                value_list = list(value)
                del value_list[index]
                value = ''.join(value_list)
                index += 2
        return value

    def __parse_number(self, value):
        """ parses attribute value passed as number """
        if '.' in value:
            try:
                value = float(value)
            except ValueError:
                pass
        else:
            try:
                value = int(value)
            except ValueError:
                pass
        return value

    def do_create(self, arg):
        """create: create [ARG]
        ARG = Class Name
        SYNOPSIS: Creates a new instance of the Class from given input ARG"""
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            for class_name, cls in CNC.items():
                if class_name == arg[0]:
                    my_obj = cls()
                    for param in arg[1:]:
                        attribute = param.split('=')
                        value = attribute[1]
                        if value[0] == '"' and value[-1] == '"':
                            value = self.__parse_string(value)
                        else:
                            value = self.__parse_number(value)
                        my_obj.bm_update(attribute[0], value)
                    my_obj.save()
                    print(my_obj.id)

    def do_show(self, arg):
        """show: show [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: Prints object of given ID from given Class"""
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            file_storage_objs = storage.all()
            for key, value in file_storage_objs.items():
                if arg[1] in key and arg[0] in key:
                    print(value)

    def do_all(self, arg):
        """all: all [ARG]
        ARG = Class
        SYNOPSIS: prints all objects of given class"""
        error = 0
        if arg:
            arg = arg.split()
            class_name = str(arg[0])
            error = self.__class_err(class_name)
        if not error:
            file_storage_objs = storage.all(class_name)
            total_objects = 0
            if class_name:
                for obj in file_storage_objs.values():
                    if isinstance(class_name, str):
                        if type(obj).__name__ == CNC[class_name].__name__:
                            total_objects += 1
                    else:
                        if type(obj).__name__ == CNC[class_name[0]].__name__:
                            total_objects += 1
            count = 0
            for obj in file_storage_objs.values():
                if isinstance(class_name, str):
                    if type(obj).__name__ == CNC[class_name].__name__:
                        count += 1
                        print(obj, end=(', ' if count < total_objects else ''))
                else:
                    if type(obj).__name__ == CNC[class_name[0]].__name__:
                        count += 1
                        print(obj, end=(', ' if count < total_objects else ''))
            else:
                total_objects = len(file_storage_objs)
                count = 0
                for obj in file_storage_objs.values():
                    print(obj, end=(', ' if count < total_objects else ''))
            print()

    def do_destroy(self, arg):
        """destroy: destroy [ARG] [ARG1]
        ARG = Class
        ARG1 = ID #
        SYNOPSIS: destroys object of given ID from given Class"""
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            file_storage_objs = storage.all()
            for key in file_storage_objs.keys():
                if arg[1] in key and arg[0] in key:
                    del file_storage_objs[key]
                    storage.save()

    def __rreplace(self, s, characters):
        for char in characters:
            s = s.replace(char, '')
        return s

    def __check_dict(self, arg):
        """checks if the arguments input has a dictionary"""
        if '{' in arg and '}' in arg:
            dict_part = arg.split('{')[1]
            dict_items = dict_part.split(', ')
            dict_list = [item.split(':') for item in dict_items]
            dictionary = {}
            for sublist in dict_list:
                key = sublist[0].strip('"\' {}')
                value = sublist[1].strip('"\' {}')
                dictionary[key] = value
            return dictionary
        else:
            return None

    def __handle_update_err(self, arg):
        """checks for all errors in update"""
        dictionary = self.__check_dict(arg)
        arg = self.__rreplace(arg, [',', '"'])
        arg = arg.split()
        error = self.__class_err(arg)
        if not error:
            error += self.__id_err(arg)
        if not error:
            valid_id = 0
            file_storage_objs = storage.all()
            for key in file_storage_objs.keys():
                if arg[1] in key and arg[0] in key:
                    key_match = key
            if len(arg) < 3:
                print(HBNBCommand.ERR[4])
            elif len(arg) < 4:
                print(HBNBCommand.ERR[5])
            else:
                return [1, arg, dictionary, file_storage_objs, key_match]
        return [0]

    def do_update(self, arg):
        """update: update [ARG] [ARG1] [ARG2] [ARG3]
        ARG = Class
        ARG1 = ID #
        ARG2 = attribute name
        ARG3 = value
        SYNOPSIS: updates attribute of an object from given Class"""
        arg_inv = self.__handle_update_err(arg)
        if arg_inv[0]:
            arg = arg_inv[1]
            dictionary = arg_inv[2]
            file_storage_objs = arg_inv[3]
            key = arg_inv[4]
            my_obj = file_storage_objs[key]
            for k, v in dictionary.items():
                my_obj.bm_update(k, v)
            storage.save()

    def do_count(self, arg):
        """count: count [ARG]
        ARG = Class
        SYNOPSIS: counts all objects of a given class"""
        error = self.__class_err(arg)
        if not error:
            file_storage_objs = storage.all(arg)
            total_objects = len(file_storage_objs)
            print(total_objects)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
