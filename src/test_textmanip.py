import unittest
from textnode import TextNode, TextType
from textmanipfunc import block_to_block_type, text_to_textnodes, markdown_to_blocks
from filemanipfunc import extract_title
from blocks import BlockType


class TestTextManip(unittest.TestCase):
    def test_block_to_block_type(self):
        heading_block = "#### Heading"
        code_block = "```Code```"
        quote_block = ">Quote\n>Quote2"
        unordered_list_block = "- one\n- two\n- three"
        ordered_list_block = "1. one\n2. two\n3. three"
        paragraph_block = "Paragraph.\nParagraph line two."
        self.assertEqual(BlockType.HEADING, block_to_block_type(heading_block))
        self.assertEqual(BlockType.CODE, block_to_block_type(code_block))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(quote_block))
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_block_type(unordered_list_block))
        self.assertEqual(BlockType.ORDERED_LIST, block_to_block_type(ordered_list_block))
        self.assertEqual(BlockType.PARAGRAPH, block_to_block_type(paragraph_block))
    def test_extract_title(self):
        md = """
# This is the title header.

## This is another header.

This is a paragraph.
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title header.")
    def test_extract_no_title(self):
        md = """
## This is the only header.
"""
        self.assertRaises(Exception, extract_title, md)
    def test_extract_out_of_order(self):
        md = """
This is a paragraph.

## This is a header 2.

# Title
"""
        title = extract_title(md)
        self.assertEqual(title, "Title")
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
    def test_markdown_to_blocks(self):
        markdown = """
# Here's the heading.

This is a **bold** paragraph.

This is a paragraph with _ital_ and `code`.
This is the same paragraph, new line.

- I am a list.
- I am part two of the list.
- List part 3.
"""
        blocks = markdown_to_blocks(markdown)
        self.assertEqual(
            [
                "# Here's the heading.",
                "This is a **bold** paragraph.",
                "This is a paragraph with _ital_ and `code`.\nThis is the same paragraph, new line.",
                "- I am a list.\n- I am part two of the list.\n- List part 3."
            ],
            blocks
        )