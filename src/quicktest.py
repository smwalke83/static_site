from splitnodes import *
from texttohtml import *
from htmlnode import *
from blocks import *
from textnode import *

md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """
print(markdown_to_html_node(md))