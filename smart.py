#!/usr/bin/env python3

import datetime
import logging
import os
import pathlib
import pickle

__all__ = ["delete", "view_trash", "clear_file", "clear", "recovery"]

logging.basicConfig(filename="sample.log", format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%Y %H:%M:%S', level=logging.INFO)


def create_trash():
    my_trash = os.path.join(str(pathlib.Path.home()), "Trash")
    data = os.path.join(my_trash, "data.pickle")
    if not os.path.exists(my_trash):
        os.mkdir(my_trash)
        with open(data, 'wb') as f:
            pickle.dump({}, f)
        logging.info("Сreated 'Trush' on " + my_trash)
    return my_trash, data


def delete(path):
    if os.path.exists(path):
        my_trash = create_trash()
        information = {os.path.basename(path): {
            'name': os.path.basename(path),
            'size': os.path.getsize(path),
            'date': datetime.datetime.now().strftime("%d-%b-%Y,%H:%M:%S"),
            'path': path}
        }
        with open(my_trash[1], 'rb') as f:
            data_new = pickle.load(f)
            data_new.update(information)
        with open(my_trash[1], 'wb') as f:
            pickle.dump(data_new, f)
        os.rename(path, os.path.join(my_trash[0], os.path.basename(path)))
        logging.info(path + " move to 'Trash'.")
    else:
        logging.info("delete(): " + path + " not found.")


def view_trash():
    my_trash = create_trash()
    with open(my_trash[1], 'rb') as f:
        data = pickle.load(f)
    print("Trash:".center(30, '-'))
    for item in data.values():
        for key, value in item.items():
            if key == 'path':
                continue
            print(key, '->', value)
        print("___" * 50)


def clear_file(file):
    my_trash = create_trash()
    path = os.path.join(my_trash[0], file)
    with open(my_trash[1], 'rb') as f:
        data = pickle.load(f)
    is_available = data.get(file)
    if os.path.exists(path) and is_available:
        _remove(path)
        with open(my_trash[1], 'rb') as f:
            data = pickle.load(f)
        data.pop(file)
        with open(my_trash[1], 'wb') as f:
            pickle.dump(data, f)
        logging.info(file + " removed from 'Trash'.")
    else:
        logging.info("clear_file: " + file + " not found in 'Trash'.")


def _remove(path):
    if os.path.isdir(path):
        for el in os.listdir(path):
            file = os.path.join(path, el)
            _remove(file)
        os.rmdir(path)
    else:
        os.remove(path)


def clear():
    my_trash = create_trash()
    files = os.listdir(my_trash[0])
    for file in files:
        if not file == 'data.pickle':
            clear_file(file)
        else:
            continue
    logging.info("'Trash' is empty.")


def recovery(file):
    my_trash = create_trash()
    if os.path.exists(os.path.join(my_trash[0], file)):
        with open(my_trash[1], 'rb') as f:
            data = pickle.load(f)
        path = data.pop(file).get('path')
        with open(my_trash[1], 'wb') as f:
            pickle.dump(data, f)
        os.rename(os.path.join(my_trash[0], file), path)
        logging.info(file + " recovery of 'Trash' in " + path)
    else:
        logging.info("recovery(): " + file + " not found.")


if __name__ == "__main__":
    # delete("/home/max/test")
    # delete("/home/max/56")
    # recovery('56')
    # view_trash()
    # clear_file('even.py')
    # view_trash()
    # clear()
    view_trash()
