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
    def test_split_image_one_node(self):
        node = TextNode("Here is one ![image](www.image.com) and ![other image](www.otherimage.com) for you.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Here is one ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.image.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("other image", TextType.IMAGE, "www.otherimage.com"),
                TextNode(" for you.", TextType.TEXT)
            ],
            new_nodes
        )
    def test_split_link_one_node(self):
        node = TextNode("Here is one [image](www.image.com) and [other image](www.otherimage.com) for you.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Here is one ", TextType.TEXT),
                TextNode("image", TextType.LINK, "www.image.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("other image", TextType.LINK, "www.otherimage.com"),
                TextNode(" for you.", TextType.TEXT)
            ],
            new_nodes
        )
    def test_split_image_multiple_nodes(self):
        nodes = [
            TextNode("Here is one ![image](www.image.com) and ![other image](www.otherimage.com) for you.", TextType.TEXT),
            TextNode("Text ![alt](link) and ![alt2](link2) here", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Here is one ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "www.image.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("other image", TextType.IMAGE, "www.otherimage.com"),
                TextNode(" for you.", TextType.TEXT),
                TextNode("Text ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "link"),
                TextNode(" and ", TextType.TEXT),
                TextNode("alt2", TextType.IMAGE, "link2"),
                TextNode(" here", TextType.TEXT)
            ],
            new_nodes
        )
    def test_split_link_multiple_nodes(self):
        nodes = [
            TextNode("Here is one [image](www.image.com) and [other image](www.otherimage.com) for you.", TextType.TEXT),
            TextNode("Text [alt](link) and [alt2](link2) here", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Here is one ", TextType.TEXT),
                TextNode("image", TextType.LINK, "www.image.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("other image", TextType.LINK, "www.otherimage.com"),
                TextNode(" for you.", TextType.TEXT),
                TextNode("Text ", TextType.TEXT),
                TextNode("alt", TextType.LINK, "link"),
                TextNode(" and ", TextType.TEXT),
                TextNode("alt2", TextType.LINK, "link2"),
                TextNode(" here", TextType.TEXT)
            ],
            new_nodes
        )
    def test_empty_nodes_image_split(self):
        nodes = [
            TextNode("![image](link) and ![image2](link2)", TextType.TEXT),
            TextNode("![image3](link)", TextType.TEXT)
        ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "link"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "link2"),
                TextNode("image3", TextType.IMAGE, "link")
            ],
            new_nodes
        )
    def test_empty_nodes_link_split(self):
        nodes = [
            TextNode("[image](link) and [image2](link2)", TextType.TEXT),
            TextNode("[image3](link)", TextType.TEXT)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.LINK, "link"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.LINK, "link2"),
                TextNode("image3", TextType.LINK, "link")
            ],
            new_nodes
        )
    def test_no_image_image_split(self):
        nodes = [
            TextNode("Hello there!", TextType.TEXT),
            TextNode("Hello there, ![image](link)", TextType.TEXT),
            TextNode("Goodbye!", TextType.TEXT)
            ]
        new_nodes = split_nodes_image(nodes)
        self.assertListEqual(
            [
                TextNode("Hello there!", TextType.TEXT),
                TextNode("Hello there, ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link"),
                TextNode("Goodbye!", TextType.TEXT)
            ],
            new_nodes
        )
    def test_no_link_link_split(self):
        nodes = [
            TextNode("Hello there!", TextType.TEXT),
            TextNode("Hello there, [image](link)", TextType.TEXT),
            TextNode("Goodbye!", TextType.TEXT)
            ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual(
            [
                TextNode("Hello there!", TextType.TEXT),
                TextNode("Hello there, ", TextType.TEXT),
                TextNode("image", TextType.LINK, "link"),
                TextNode("Goodbye!", TextType.TEXT)
            ],
            new_nodes
        )
    def text_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
            new_nodes
        )
    def test_text_to_textnodes_different_order(self):
        text = "_start_ with ital, then ![image](image link), **bold**, then [link](url), finally `code`."
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("start", TextType.ITALIC),
                TextNode(" with ital, then ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "image link"),
                TextNode(", ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", then ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(", finally ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(".", TextType.TEXT)
            ],
            new_nodes
        )
    def test_text_to_textnodes_repeats(self):
        text = "**bold** normal _ital_ ![img](link) ![img2](link2) **bold** _ital_ normal"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" normal ", TextType.TEXT),
                TextNode("ital", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "link"),
                TextNode(" ", TextType.TEXT),
                TextNode("img2", TextType.IMAGE, "link2"),
                TextNode(" ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" ", TextType.TEXT),
                TextNode("ital", TextType.ITALIC),
                TextNode(" normal", TextType.TEXT)
            ],
            new_nodes
        )
    def test_text_to_textnode_no_split(self):
        text = "Hello, world! No special stuff here!"
        nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode(text, TextType.TEXT)], nodes)


#if __name__ == "__main__":
    #unittest.main()                These two lines are only necessary when you want to run just this specific file, not when using ./test.sh