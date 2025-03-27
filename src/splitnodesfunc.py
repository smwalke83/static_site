from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
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
