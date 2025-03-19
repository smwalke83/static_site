from textnode import TextNode, TextType

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
