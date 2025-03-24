from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from texttohtml import *
from blocks import *
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_node_list = []
    for node in old_nodes:
        match node.text_type:
            case TextType.TEXT:
                if delimiter in node.text:
                    nodes = node.text.split(delimiter)
                    if len(nodes) % 2 == 0:
                        raise Exception("No closing delimiter")
                    for string in nodes:
                            if nodes.index(string) == 0:
                                if string:
                                    text_node_list.append(TextNode(string, TextType.TEXT)) 
                            elif nodes.index(string) % 2 == 1:
                                text_node_list.append(TextNode(string, text_type))
                            else:
                                if string:
                                    text_node_list.append(TextNode(string, TextType.TEXT))
                else:
                    text_node_list.append(node)
            case _:
                text_node_list.append(node)
    return text_node_list

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
        elif len(matches) == 1:
            sections = node.text.split(f"![{matches[0][0]}]({matches[0][1]})", 1)
            if sections[0] == "" and sections[1] == "":
                new_nodes.append(TextNode(matches[0][0], TextType.IMAGE, matches[0][1]))
            elif sections[0] == "":
                new_nodes.append(TextNode(matches[0][0], TextType.IMAGE, matches[0][1]))
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
            elif sections[1] == "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(matches[0][0], TextType.IMAGE, matches[0][1]))
            else:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(matches[0][0], TextType.IMAGE, matches[0][1]))
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
        else:
            for tuple in matches:
                if matches.index(tuple) == 0:
                    sections = node.text.split(f"![{tuple[0]}]({tuple[1]})", 1)
                    new_text = sections[1]
                    if sections[0] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                    else:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                elif matches.index(tuple) == len(matches) - 1:
                    sections = new_text.split(f"![{tuple[0]}]({tuple[1]})", 1)
                    if sections[0] == "" and sections[1] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                    elif sections[0] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                        new_nodes.append(TextNode(sections[1], TextType.TEXT))
                    elif sections[1] == "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                    else:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                        new_nodes.append(TextNode(sections[1], TextType.TEXT))
                else:
                    sections = new_text.split(f"![{tuple[0]}]({tuple[1]})", 1)
                    new_text = sections[1]
                    if sections[0] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
                    else:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.IMAGE, tuple[1]))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            new_nodes.append(node)
        elif len(matches) == 1:
            sections = node.text.split(f"[{matches[0][0]}]({matches[0][1]})", 1)
            if sections[0] == "" and sections[1] == "":
                new_nodes.append(TextNode(matches[0][0], TextType.LINK, matches[0][1]))
            elif sections[0] == "":
                new_nodes.append(TextNode(matches[0][0], TextType.LINK, matches[0][1]))
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
            elif sections[1] == "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(matches[0][0], TextType.LINK, matches[0][1]))
            else:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
                new_nodes.append(TextNode(matches[0][0], TextType.LINK, matches[0][1]))
                new_nodes.append(TextNode(sections[1], TextType.TEXT))
        else:
            for tuple in matches:
                if matches.index(tuple) == 0:
                    sections = node.text.split(f"[{tuple[0]}]({tuple[1]})", 1)
                    new_text = sections[1]
                    if sections[0] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                    else:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                elif matches.index(tuple) == len(matches) - 1:
                    sections = new_text.split(f"[{tuple[0]}]({tuple[1]})", 1)
                    if sections[0] == "" and sections[1] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                    elif sections[0] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                        new_nodes.append(TextNode(sections[1], TextType.TEXT))
                    elif sections[1] == "":
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                    else:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                        new_nodes.append(TextNode(sections[1], TextType.TEXT))
                else:
                    sections = new_text.split(f"[{tuple[0]}]({tuple[1]})", 1)
                    new_text = sections[1]
                    if sections[0] == "":
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
                    else:
                        new_nodes.append(TextNode(sections[0], TextType.TEXT))
                        new_nodes.append(TextNode(tuple[0], TextType.LINK, tuple[1]))
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes
    
def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    for block in block_list:
        block_list[block_list.index(block)] = block.strip()
        if block == "":
            block_list.remove(block)
    return block_list

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    HTML_node_list = []
    for block in block_list:
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                new_block = block.replace("\n", " ")
                tag = "p"
                children = text_to_children(new_block)
                if len(children) == 1:
                    HTML_node_list.append(LeafNode(tag, children[0].value, children[0].props))
                else:
                    HTML_node_list.append(ParentNode(tag, children))
            case BlockType.HEADING:
                if block.startswith("# "):
                    tag = "h1"
                if block.startswith("## "):
                    tag = "h2"
                if block.startswith("### "):
                    tag = "h3"
                if block.startswith("#### "):
                    tag = "h4"
                if block.startswith("##### "):
                    tag = "h5"
                if block.startswith("###### "):
                    tag = "h6"
                children = text_to_children(block)
                if len(children == 1):
                    HTML_node_list.append(LeafNode(tag, children[0].value, children[0].props))
                else:
                    HTML_node_list.append(ParentNode(tag, children))
            case BlockType.QUOTE:
                tag = "blockquote"
                children = text_to_children(block)
                if len(children == 1):
                    HTML_node_list.append(LeafNode(tag, children[0].value, children[0].props))
                else:
                    HTML_node_list.append(ParentNode(tag, children))
            case BlockType.UNORDERED_LIST:
                tag = "ul"
                children = text_to_children(block)
                if len(children == 1):
                    HTML_node_list.append(LeafNode(tag, children[0].value, children[0].props))
                else:
                    HTML_node_list.append(ParentNode(tag, children))
            case BlockType.ORDERED_LIST:
                tag = "ol"
                children = text_to_children(block)
                if len(children == 1):
                    HTML_node_list.append(LeafNode(tag, children[0].value, children[0].props))
                else:
                    HTML_node_list.append(ParentNode(tag, children))
            case BlockType.CODE:
                tag = "pre"
                text_nodes = text_to_textnodes(block)
                HTML_node = text_node_to_html_node(text_nodes[0])
                HTML_node_list.append(ParentNode(tag, HTML_node))
    return ParentNode("div", HTML_node_list)
                
'''
Things still to implement: Replace line breaks in lists (within single list items) with space, replace line breaks within block quotes with spaces.
Code blocks maintain their line breaks.
Unordered lists get the <ul> tag, but each list item needs the <li> tag. Same for Ordered Lists.
Code blocks need a <pre> tag and then a <code> tag (wrote test function, getting "no closing delimiter" error)
'''          

        
