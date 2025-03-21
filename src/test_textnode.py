import unittest
from textnode import TextNode, TextType
from splitnodes import *

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
    def test_split_bold(self):
        old_nodes = [
            TextNode("Put some **bold** in it", TextType.TEXT),
            TextNode("Put no bold in it", TextType.TEXT),
            TextNode("Put **even more** of that **bold** in it", TextType.TEXT)
        ]
        expected_new_nodes = [
            TextNode("Put some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" in it", TextType.TEXT),
            TextNode("Put no bold in it", TextType.TEXT),
            TextNode("Put ", TextType.TEXT),
            TextNode("even more", TextType.BOLD),
            TextNode(" of that ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" in it", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, expected_new_nodes)
    def test_split_ital(self):
        old_nodes = [
            TextNode("Put some _italics_ in it", TextType.TEXT),
            TextNode("Put no italics in it", TextType.TEXT),
            TextNode("Put _even more_ of that _italics_ in it", TextType.TEXT)
        ]
        expected_new_nodes = [
            TextNode("Put some ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT),
            TextNode("Put no italics in it", TextType.TEXT),
            TextNode("Put ", TextType.TEXT),
            TextNode("even more", TextType.ITALIC),
            TextNode(" of that ", TextType.TEXT),
            TextNode("italics", TextType.ITALIC),
            TextNode(" in it", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, expected_new_nodes)
    def test_split_code(self):
        old_nodes = [
            TextNode("Put some `code` in it", TextType.TEXT),
            TextNode("Put no code in it", TextType.TEXT),
            TextNode("Put `even more` of that `code` in it", TextType.TEXT)
        ]
        expected_new_nodes = [
            TextNode("Put some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in it", TextType.TEXT),
            TextNode("Put no code in it", TextType.TEXT),
            TextNode("Put ", TextType.TEXT),
            TextNode("even more", TextType.CODE),
            TextNode(" of that ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in it", TextType.TEXT)
        ]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, expected_new_nodes)
    def test_split_multiple(self):
        old_nodes = [
            TextNode("Put **some** `code` _in_ it", TextType.TEXT),
            TextNode("Put no code in it", TextType.TEXT)
        ]
        expected_new_nodes = [
            TextNode("Put ", TextType.TEXT),
            TextNode("some", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("in", TextType.ITALIC),
            TextNode(" it", TextType.TEXT),
            TextNode("Put no code in it", TextType.TEXT),
        ]
        bold_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        bold_and_code = split_nodes_delimiter(bold_nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(bold_and_code, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, expected_new_nodes)
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_links(self):
        text = "This is text with a link [to link](www.link.com)"
        matches = extract_markdown_links(text)
        self.assertEqual([("to link", "www.link.com")], matches)
    def test_multiple_images(self):
        text = "This is text with ![this image](www.thisimage.com) and ![that image](www.thatimage.com)"
        matches = extract_markdown_images(text)
        self.assertEqual([("this image", "www.thisimage.com"), ("that image", "www.thatimage.com")], matches)
    def test_multiple_links(self):
        text = "This has a link [to link](www.link.com) and another link [to other link](www.otherlink.com)"
        matches = extract_markdown_links(text)
        self.assertEqual([("to link", "www.link.com"), ("to other link", "www.otherlink.com")], matches)
    def test_no_tags(self):
        text = "This is just text"
        matches = extract_markdown_images(text)
        self.assertEqual([], matches)

#if __name__ == "__main__":
    #unittest.main()                These two lines are only necessary when you want to run just this specific file, not when using ./test.sh