from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode
import sys
import os
import shutil

def main():
    node = TextNode("My Text", "My Text Type", "https://www.fakeurl.com")
    print(node)


def copy_to_public(source):
    shutil.rmtree("public")
    os.mkdir("public")
    new_filepath = "public"
    if os.path.isfile(source):
        shutil.copy(source, new_filepath)
    else:
        contents = listdir(source)
        for item in contents:
            os.path.join(new_filepath, item)
            copy_to_public(item)
    

    # This is untested, but clearly it cannot delete the public directory every loop.
    
main()