from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode

def main():
    node = TextNode("My Text", "My Text Type", "https://www.fakeurl.com")
    print(node)



main()