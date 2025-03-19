from enum import Enum
from textnode import TextNode, TextType

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if self.props != None:
            prop_html = " "
            for prop in self.props:
                prop_html += f'{prop}="{self.props[prop]}" '
            return prop_html
        return None
    def __repr__(self):
        return f"HTMLNode - \nTag: {self.tag} \nValue: {self.value} \nChildren: {self.children} \nProps: {self.props}"
    def __eq__(self, node):
        if self.tag == node.tag and self.value == node.value and self.children == node.children and self.props == node.props:
            return True
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        super().__init__(tag, value, None, props)
    def to_html(self):
        if self.value == None:
            raise ValueError("leaf node must have value")
        if self.tag == None:
            return self.value
        return f"<{self.tag}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, children, props)
    def to_html(self):
        if self.tag == None:
            raise ValueError("parent node must have tag")
        if self.children == None:
            raise ValueError("parent node must have children")
        html = f"<{self.tag}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
    

