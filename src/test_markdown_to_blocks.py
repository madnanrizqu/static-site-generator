import unittest
from markdown_to_blocks import markdown_to_blocks, BlockType, block_to_block_type


class TestMarkdownToBlocks(unittest.TestCase):
    def test_multiple_rows(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_row(self):
        md = """
This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
"""

        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
            ],
        )

    def test_no_row(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_excessive_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_trailing_spaces(self):
        md = "   This is a block with leading and trailing spaces.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a block with leading and trailing spaces."])


class TestBlockToBlockType(unittest.TestCase):
    def test_heading_one(self):
        block = "# Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "#Heading 1"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_two(self):
        block = "## Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "##Heading 2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_three(self):
        block = "### Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "###Heading 3"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_four(self):
        block = "#### Heading 4"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "####Heading 4"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_five(self):
        block = "##### Heading 5"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "#####Heading 5"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_six(self):
        block = "###### Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "######Heading 6"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_multiline_code(self):
        block = '```\nprint("Hello")\nprint("World")\n```'
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_multiline_code_no_leading_space(self):
        block = '```print("Hello")\nprint("World")\n```'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_multiline_code_no_trailing_ticks(self):
        block = '```\nprint("Hello")\nprint("World")'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_with_space(self):
        block = "> I'am\n" + "> Learning\n" + "> In lines\n"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_some_no_space(self):
        block = ">I'am\n" + "> Learning\n" + "> In lines\n"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_all_no_space(self):
        block = ">I'am\n" + ">Learning\n" + ">In lines\n"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_first_no_proper_start(self):
        block = "I'am\n" + "> Learning\n" + "> In lines\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_some_no_proper_start(self):
        block = "> I'am\n" + "Learning\n" + "> In lines\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Apple\n" + "- Banana\n" + "- Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        block = "- Apple\n"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space_on_first(self):
        block = "-Apple\n" + "- Banana\n" + "- Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_no_space_on_other(self):
        block = "-Apple\n" + "- Banana\n" + "-Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_no_hyphen_on_first(self):
        block = "Apple\n" + "- Banana\n" + "- Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_no_hyphen_on_other(self):
        block = "- Apple\n" + "Banana\n" + "- Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. Apple\n" + "2. Banana\n" + "3. Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_no_start_with_one(self):
        block = "0. Apple\n" + "1. Banana\n" + "2. Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_increment(self):
        block = "1. Apple\n" + "5. Banana\n" + "3. Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space_on_first(self):
        block = "1.Apple\n" + "2. Banana\n" + "3. Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space_on_other(self):
        block = "1. Apple\n" + "2.Banana\n" + "3. Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_dot_on_first(self):
        block = "1 Apple\n" + "2. Banana\n" + "3. Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_dot_on_other(self):
        block = "1. Apple\n" + "2 Banana\n" + "3. Orange\n"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
