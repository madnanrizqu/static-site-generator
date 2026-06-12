import unittest
from markdown_to_blocks import markdown_to_blocks, BlockType, block_to_block_type, markdown_to_html_node


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

    def test_multiline_code_no_trailing_ticks(self):
        block = '```\nprint("Hello")\nprint("World")'
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_with_space(self):
        block = "> I'am\n" + "> Learning\n" + "> In lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_some_no_space(self):
        block = ">I'am\n" + "> Learning\n" + "> In lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_all_no_space(self):
        block = ">I'am\n" + ">Learning\n" + ">In lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_first_no_proper_start(self):
        block = "I'am\n" + "> Learning\n" + "> In lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block_some_no_proper_start(self):
        block = "> I'am\n" + "Learning\n" + "> In lines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block = "- Apple\n" + "- Banana\n" + "- Orange"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_single_item(self):
        block = "- Apple"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_unordered_list_no_space_on_first(self):
        block = "-Apple\n" + "- Banana\n" + "- Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_no_space_on_other(self):
        block = "-Apple\n" + "- Banana\n" + "-Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_no_hyphen_on_first(self):
        block = "Apple\n" + "- Banana\n" + "- Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_no_hyphen_on_other(self):
        block = "- Apple\n" + "Banana\n" + "- Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block = "1. Apple\n" + "2. Banana\n" + "3. Orange"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_ordered_list_no_start_with_one(self):
        block = "0. Apple\n" + "1. Banana\n" + "2. Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_increment(self):
        block = "1. Apple\n" + "5. Banana\n" + "3. Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space_on_first(self):
        block = "1.Apple\n" + "2. Banana\n" + "3. Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_space_on_other(self):
        block = "1. Apple\n" + "2.Banana\n" + "3. Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_dot_on_first(self):
        block = "1 Apple\n" + "2. Banana\n" + "3. Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_no_dot_on_other(self):
        block = "1. Apple\n" + "2 Banana\n" + "3. Orange"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

class TestMarkdownToHTMLNode(unittest.TestCase):

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
    
    def test_headings(self):
        md = "# Heading 1"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1</h1></div>")

    def test_heading_two(self):
        md = "## Heading 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h2>Heading 2</h2></div>")

    def test_heading_three(self):
        md = "### Heading 3"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h3>Heading 3</h3></div>")

    def test_heading_four(self):
        md = "#### Heading 4"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h4>Heading 4</h4></div>")

    def test_heading_five(self):
        md = "##### Heading 5"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h5>Heading 5</h5></div>")

    def test_heading_six(self):
        md = "###### Heading 6"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h6>Heading 6</h6></div>")

    def test_heading_with_italic(self):
        md = "# Heading 1 with _italic_ text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1 with <i>italic</i> text</h1></div>")

    def test_heading_with_bold(self):
        md = "# Heading 1 with **bold** text"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1 with <b>bold</b> text</h1></div>")

    def test_heading_with_link(self):
        md = "# Heading 1 with a [link](https://example.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1 with a <a href=\"https://example.com\">link</a></h1></div>")

    def test_heading_with_image(self):
        md = "# Heading 1 with an image ![alt](https://example.com/img.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading 1 with an image <img src=\"https://example.com/img.png\" alt=\"alt\"></img></h1></div>")

    def test_heading_with_all_mixed(self):
        md = "# Heading **bold** _italic_ [link](https://example.com) ![img](https://example.com/a.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Heading <b>bold</b> <i>italic</i> <a href=\"https://example.com\">link</a> <img src=\"https://example.com/a.png\" alt=\"img\"></img></h1></div>")

    def test_blockquote(self):
        md = "> Blockquote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Blockquote</blockquote></div>")
    
    def test_multiple_blockquote(self):
        md = "> Blockquote \n\n> Blockquote 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>Blockquote</blockquote><blockquote>Blockquote 2</blockquote></div>")

    def test_blockquote_multiline(self):
        md = """> I'am
> learning
> in lines"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>I'am learning in lines</blockquote></div>")

    def test_blockquote_with_italic(self):
        md = "> This is _italic_ blockquote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is <i>italic</i> blockquote</blockquote></div>")

    def test_blockquote_with_bold(self):
        md = "> This is **bold** blockquote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is <b>bold</b> blockquote</blockquote></div>")

    def test_blockquote_multiline_with_italic(self):
        md = """> This is _italic_
> text in blockquote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is <i>italic</i> text in blockquote</blockquote></div>")

    def test_blockquote_multiline_with_bold(self):
        md = """> This is **bold**
> text in blockquote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is <b>bold</b> text in blockquote</blockquote></div>")

    def test_blockquote_with_link(self):
        md = "> This is a [link](https://example.com) in blockquote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a <a href=\"https://example.com\">link</a> in blockquote</blockquote></div>")

    def test_blockquote_multiline_with_link(self):
        md = """> This is a [link](https://example.com)
> in blockquote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is a <a href=\"https://example.com\">link</a> in blockquote</blockquote></div>")

    def test_blockquote_with_image(self):
        md = "> This is an ![alt text](https://example.com/image.png) in blockquote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is an <img src=\"https://example.com/image.png\" alt=\"alt text\"></img> in blockquote</blockquote></div>")

    def test_blockquote_multiline_with_image(self):
        md = """> This is an ![alt text](https://example.com/image.png)
> in blockquote"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><blockquote>This is an <img src=\"https://example.com/image.png\" alt=\"alt text\"></img> in blockquote</blockquote></div>")

    def test_unordered_list_single_items(self):
        md = "- Apple\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Apple</li></ul></div>")

    def test_unordered_list_with_link(self):
        md = "- This is a [link](https://example.com) of a website"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is a <a href=\"https://example.com\">link</a> of a website</li></ul></div>")

    def test_unordered_list_with_image(self):
        md = "- This is an Image: ![alt text](https://example.com/image.png) pretty good"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is an Image: <img src=\"https://example.com/image.png\" alt=\"alt text\"></img> pretty good</li></ul></div>")

    def test_unordered_list_with_bold(self):
        md = "- This is a **bold text** here"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is a <b>bold text</b> here</li></ul></div>")

    def test_unordered_list_with_italic(self):
        md = "- This is an _italic text_ here"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is an <i>italic text</i> here</li></ul></div>")
    
    def test_unordered_list_single_with_all_mixed(self):
        md = "- This is a **bold** text with a _italic_ text with a [link](https://example.com) to a website and an image ![img](https://example.com/a.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is a <b>bold</b> text with a <i>italic</i> text with a <a href=\"https://example.com\">link</a> to a website and an image <img src=\"https://example.com/a.png\" alt=\"img\"></img></li></ul></div>")

    def test_unordered_list_multi_items(self):
        md = "- Apple\n" + "- Orange\n" + "- Banana"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>Apple</li><li>Orange</li><li>Banana</li></ul></div>")

    def test_unordered_list_multi_with_link(self):
        md = "- [link](https://example.com) here\n- another [link](https://example.org)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li><a href=\"https://example.com\">link</a> here</li><li>another <a href=\"https://example.org\">link</a></li></ul></div>")

    def test_unordered_list_multi_with_image(self):
        md = "- ![img](https://example.com/a.png) here\n- ![img2](https://example.com/b.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li><img src=\"https://example.com/a.png\" alt=\"img\"></img> here</li><li><img src=\"https://example.com/b.png\" alt=\"img2\"></img></li></ul></div>")

    def test_unordered_list_multi_with_bold(self):
        md = "- **bold** here\n- also **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li><b>bold</b> here</li><li>also <b>bold</b></li></ul></div>")

    def test_unordered_list_multi_with_italic(self):
        md = "- _italic_ here\n- also _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li><i>italic</i> here</li><li>also <i>italic</i></li></ul></div>")

    def test_unordered_list_multi_with_all_mixed(self):
        md = "- This is a **bold** and _italic_ text\n- Here is a [link](https://example.com) and an image ![img](https://example.com/a.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>This is a <b>bold</b> and <i>italic</i> text</li><li>Here is a <a href=\"https://example.com\">link</a> and an image <img src=\"https://example.com/a.png\" alt=\"img\"></img></li></ul></div>")
    
    def test_ordered_list_single_item(self):
        md = "1. Apple"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Apple</li></ol></div>")

    def test_ordered_list_single_with_bold(self):
        md = "1. This is a **bold text** here"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This is a <b>bold text</b> here</li></ol></div>")

    def test_ordered_list_single_with_italic(self):
        md = "1. This is an _italic text_ here"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This is an <i>italic text</i> here</li></ol></div>")

    def test_ordered_list_single_with_link(self):
        md = "1. This is a [link](https://example.com) of a website"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This is a <a href=\"https://example.com\">link</a> of a website</li></ol></div>")

    def test_ordered_list_single_with_image(self):
        md = "1. This is an Image: ![alt text](https://example.com/image.png) pretty good"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This is an Image: <img src=\"https://example.com/image.png\" alt=\"alt text\"></img> pretty good</li></ol></div>")

    def test_ordered_list_single_with_all_mixed(self):
        md = "1. This is a **bold** text with a _italic_ text with a [link](https://example.com) to a website and an image ![img](https://example.com/a.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This is a <b>bold</b> text with a <i>italic</i> text with a <a href=\"https://example.com\">link</a> to a website and an image <img src=\"https://example.com/a.png\" alt=\"img\"></img></li></ol></div>")

    def test_ordered_list_multi_items(self):
        md = "1. Apple" + "\n2. Banana" + "\n3. Orange"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>Apple</li><li>Banana</li><li>Orange</li></ol></div>")

    def test_ordered_list_multi_with_bold(self):
        md = "1. **bold** here\n2. also **bold**"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li><b>bold</b> here</li><li>also <b>bold</b></li></ol></div>")

    def test_ordered_list_multi_with_italic(self):
        md = "1. _italic_ here\n2. also _italic_"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li><i>italic</i> here</li><li>also <i>italic</i></li></ol></div>")

    def test_ordered_list_multi_with_link(self):
        md = "1. [link](https://example.com) here\n2. another [link](https://example.org)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li><a href=\"https://example.com\">link</a> here</li><li>another <a href=\"https://example.org\">link</a></li></ol></div>")

    def test_ordered_list_multi_with_image(self):
        md = "1. ![img](https://example.com/a.png) here\n2. ![img2](https://example.com/b.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li><img src=\"https://example.com/a.png\" alt=\"img\"></img> here</li><li><img src=\"https://example.com/b.png\" alt=\"img2\"></img></li></ol></div>")

    def test_ordered_list_multi_with_all_mixed(self):
        md = "1. This is a **bold** and _italic_ text\n2. Here is a [link](https://example.com) and an image ![img](https://example.com/a.png)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ol><li>This is a <b>bold</b> and <i>italic</i> text</li><li>Here is a <a href=\"https://example.com\">link</a> and an image <img src=\"https://example.com/a.png\" alt=\"img\"></img></li></ol></div>")
    
    def test_mixed_blocks(self):
        md = """# Heading

A paragraph with **bold** and _italic_ text.

- Unordered item 1
- Unordered item 2

1. Ordered item 1
2. Ordered item 2

> A blockquote

```
code block
```"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>A paragraph with <b>bold</b> and <i>italic</i> text.</p><ul><li>Unordered item 1</li><li>Unordered item 2</li></ul><ol><li>Ordered item 1</li><li>Ordered item 2</li></ol><blockquote>A blockquote</blockquote><pre><code>code block\n</code></pre></div>",
        )

    def test_empty_doc(self):
        md = ""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div></div>")

if __name__ == "__main__":
    unittest.main()
