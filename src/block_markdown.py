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
    if re.match(r"^#{1,6} .+", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("```"):
        return BlockType.CODE
    if block.startswith("> ") or block.startswith(">"):
        all_lines = block.split("\n")
        is_valid = True
        for line in all_lines:
            if line == "" or line.startswith("> ") or line.startswith(">"):
                continue
            else:
                is_valid = False
                break

        if is_valid:
            return BlockType.QUOTE
    if block.startswith("- "):
        all_lines = block.split("\n")
        is_valid = True
        for line in all_lines:
            if line == "" or line.startswith("- "):
                continue
            else:
                is_valid = False
                break

        if is_valid:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        current_num = 1
        all_lines = block.split("\n")
        is_valid = True
        for line in all_lines:
            if line == "" or line.startswith(f"{current_num}. "):
                current_num += 1
            else:
                is_valid = False
                break

        if is_valid:
            return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH
