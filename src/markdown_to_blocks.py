from enum import Enum
import re
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import text_to_textnodes


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


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)

    child_nodes = []
    for text_node in text_nodes:
        child_nodes.append(text_node_to_html_node(text_node))

    return child_nodes


def block_to_heading_node(block: str) -> ParentNode:
    level = block.count("#")
    text = block.lstrip("#").strip()
    flattened = " ".join(line.strip() for line in text.split("\n"))
    return ParentNode(f"h{level}", text_to_children(flattened))


def block_to_paragraph_node(block: str) -> ParentNode:
    text = " ".join(line.strip() for line in block.split("\n"))
    return ParentNode("p", text_to_children(text))


def block_to_code_node(block: str) -> ParentNode:
    code_text = block.lstrip("```\n").rstrip("```")
    code_node = LeafNode("code", code_text)
    return ParentNode("pre", [code_node])


def block_to_quote_node(block: str) -> ParentNode:
    lines = block.split("\n")
    stripped = []
    for line in lines:
        if line.startswith("> "):
            stripped.append(line[2:])
        else:
            stripped.append(line[1:])
    text = " ".join(line.strip() for line in stripped)
    return ParentNode("blockquote", text_to_children(text))


def block_to_unordered_list_node(block: str) -> ParentNode:
    children = []
    for line in block.split("\n"):
        children.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", children)


def block_to_ordered_list_node(block: str) -> ParentNode:
    children = []
    for line in block.split("\n"):
        text = re.sub(r"^\d+\.\s*", "", line)
        children.append(ParentNode("li", text_to_children(text)))
    return ParentNode("ol", children)


def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    result: list[HTMLNode] = []
    for block in blocks:
        type = block_to_block_type(block)

        if type == BlockType.HEADING:
            result.append(block_to_heading_node(block))
        elif type == BlockType.PARAGRAPH:
            result.append(block_to_paragraph_node(block))
        elif type == BlockType.CODE:
            result.append(block_to_code_node(block))
        elif type == BlockType.QUOTE:
            result.append(block_to_quote_node(block))
        elif type == BlockType.UNORDERED_LIST:
            result.append(block_to_unordered_list_node(block))
        elif type == BlockType.ORDERED_LIST:
            result.append(block_to_ordered_list_node(block))

    return ParentNode("div", result)
