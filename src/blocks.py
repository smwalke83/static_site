from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def block_to_block_type(block):
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif block[0] + block[1] + block[2] == "```" and block[len(block) - 1] + block[len(block) - 2] + block[len(block) - 3] == "```":
        return BlockType.CODE
    elif block[0] == ">":
        return BlockType.QUOTE
    elif block[0] == "-" and block[1] == " ":
        return BlockType.UNORDERED_LIST
    elif block[0] == "1" and block[1] == "." and block[2] == " ":
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

        # need to revisit and split block into lines to check code, quote, and lists
    