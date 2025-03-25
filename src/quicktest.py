from splitnodes import *
from texttohtml import *
from htmlnode import *
from blocks import *
from textnode import *
import sys, os, shutil

"""
def copy_to_public(source):
    #shutil.rmtree("public")
    #os.mkdir("public")
    if os.path.isfile(source):
        shutil.copy(source, filepath)
    else:
        filepath = "public"
        contents = os.listdir(source)
        for item in contents:
            if os.path.isfile(item):
                shutil.copy(item, filepath)
            else:
                filepath = os.path.join(filepath, item)
                os.mkdir(filepath)
                copy_to_public(item)
"""


def copy_to_public(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    if not os.path.exists(destination):
        os.mkdir(destination)
    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_to_public(source_path, dest_path)
copy_to_public("static", "public")





