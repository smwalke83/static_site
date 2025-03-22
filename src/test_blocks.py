import unittest
from blocks import *

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