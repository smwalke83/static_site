from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType
from blocks import BlockType
from splitnodesfunc import split_nodes_delimiter, split_nodes_image, split_nodes_link
import re


def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    for block in block_list:
        block_list[block_list.index(block)] = block.strip()
        if block == "":
            block_list.remove(block)
    return block_list

def markdown_to_html_node(markdown):
    block_list = markdown_to_blocks(markdown)
    HTML_node_list = []
    for block in block_list:
        HTML_node_list.append(block_to_html_node(block))
    return ParentNode("div", HTML_node_list)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    leaf_nodes = []
    for node in text_nodes:
        leaf_nodes.append(text_node_to_html_node(node))
    return leaf_nodes

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

def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, "_", TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, "`", TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    link_nodes = split_nodes_link(image_nodes)
    return link_nodes

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            props = {
                "href" : text_node.url
            }
            return LeafNode("a", text_node.text, props)
        case TextType.IMAGE:
            props = {
                "src" : text_node.url,
                "alt" : text_node.text
            }
            return LeafNode("img", "", props)
        case _:
            raise Exception

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH