import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_url(self):
        node = TextNode("Node", TextType.ITALIC, "www.wrongurl.com")
        node2 = TextNode("Node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_urls(self):
        node = TextNode("Word", TextType.BOLD, "www.www.www")
        node2 = TextNode("Word", TextType.BOLD, "www.www.www")
        self.assertEqual(node, node2)
    def test_texttype(self):
        node = TextNode("Word", TextType.BOLD, "www.www.www")
        node2 = TextNode("Word", TextType.ITALIC, "www.www.www")
        self.assertNotEqual(node, node2)
    def test_texteq(self):
        node = TextNode("Word", TextType.ITALIC)
        node2 = TextNode("Text", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
#if __name__ == "__main__":
    #unittest.main()                These two lines are only necessary when you want to run just this specific file, not when using ./test.sh