from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    text_node_list = []
    for node in old_nodes:
        #if node.type not TextType.TEXT:
            #text_node_list.append(node)
        if delimiter in node.text:
            nodes = node.text.split(delimiter)
            if len(nodes) == 2:
                raise Exception("No closing delimiter")
            for string in nodes:
                    if nodes.index(string) == 0:
                        text_node_list.append(TextNode(string, TextType.TEXT)) 
                    elif nodes.index(string) % 2 == 1:
                        text_node_list.append(TextNode(string, text_type))
                    else:
                        text_node_list.append(TextNode(string, TextType.TEXT))
        else:
            text_node_list.append(node)
    return text_node_list

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if len(extract_markdown_images(node.text)) == 0:
            new_nodes.append(node)
        elif len(extract_markdown_images(node.text)) == 1:
            matches = extract_markdown_images(node.text)
            sections = node.text.split(f"![{matches[0][0]}]({matches[0][1]})")
            new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(matches[0][0]), TextType.IMAGE, matches[0][1])
            new_nodes.append(TextNode(sections[1], TextType.TEXT))
        #Hello Neo. This function is incomplete and untested. It needs an else statement to deal with multiple extractions from the extract_markdown_images function.

def split_nodes_link(old_nodes):
    
def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

