import unittest
from blocks import *
from main import *

class TestBlocks(unittest.TestCase):
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