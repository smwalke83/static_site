from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
import sys
import os
import shutil

def main():
    copy_to_public("static", "public")


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
    


    
main()