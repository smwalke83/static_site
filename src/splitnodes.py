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
        HTML_node_list.append(block_to_html_node(block))
    return ParentNode("div", HTML_node_list)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return olist_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return ulist_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)

def paragraph_to_html_node(block):
    tag = "p"
    paragraph = block.replace("\n", " ")
    children = text_to_children(paragraph)
    return ParentNode(tag, children)

def heading_to_html_node(block):
    if block.startswith("# "):
        tag = "h1"
    elif block.startswith("## "):
        tag = "h2"
    elif block.startswith("### "):
        tag = "h3"
    elif block.startswith("#### "):
        tag = "h4"
    elif block.startswith("##### "):
        tag = "h5"
    elif block.startswith("###### "):
        tag = "h6"
    else:
        raise ValueError("invalid heading level")
    children = text_to_children(block.lstrip("#").strip())
    return ParentNode(tag, children)

def code_to_html_node(block):
    tag = "pre"
    code = block.strip("```").strip()
    node = TextNode(code, TextType.TEXT)
    leaf_node = text_node_to_html_node(node)
    code_node = ParentNode("code", [leaf_node])
    return ParentNode(tag, [code_node])

def olist_to_html_node(block):
    tag = "ol"
    list_lines = block.split("\n")
    nodes = []
    for line in list_lines:
        children = text_to_children(line[3:])
        nodes.append(ParentNode("li", children))
    return ParentNode(tag, nodes)

def ulist_to_html_node(block):
    tag = "ul"
    list_lines = block.split("\n")
    nodes = []
    for line in list_lines:
        children = text_to_children(line[2:])
        nodes.append(ParentNode("li", children))
    return ParentNode(tag, nodes)

def quote_to_html_node(block):
    tag = "blockquote"
    quote_lines = block.split("\n")
    new_lines = []
    for line in quote_lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    quote = " ".join(new_lines)
    children = text_to_children(quote)
    return ParentNode(tag, children)

     

        
