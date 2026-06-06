from enum import Enum
import re


def markdown_to_blocks(markdown: str) -> list[str]:
    rows = markdown.split("\n\n")
    return [row.strip() for row in rows if row.strip()]


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if len(lines) == 1 and re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING
    if len(lines) > 1 and block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        if all(line.startswith(">") for line in lines):
            return BlockType.QUOTE
    if block.startswith("- "):
        if all(line.startswith("- ") for line in lines):
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        current_num = 1
        is_valid = True
        for line in lines:
            if not line.startswith(f"{current_num}. "):
                is_valid = False
                break
            current_num += 1

        if is_valid:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
