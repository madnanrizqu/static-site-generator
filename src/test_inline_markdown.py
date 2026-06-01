import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_link,
    split_nodes_image,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code_block(self):
        node = TextNode("This is text with a `code block` section", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" section", TextType.TEXT),
            ],
        )

    def test_split_double_code_block(self):
        node = TextNode(
            "This is text with a `code block one` section and `code block two` section",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block one", TextType.CODE),
                TextNode(" section and ", TextType.TEXT),
                TextNode("code block two", TextType.CODE),
                TextNode(" section", TextType.TEXT),
            ],
        )

    def test_split_bold_block(self):
        node = TextNode("This is text with a **bolded phrase** section", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase", TextType.BOLD),
                TextNode(" section", TextType.TEXT),
            ],
        )

    def test_split_double_bold_block(self):
        node = TextNode(
            "This is text with a **bolded phrase one** section and **bolded phrase two** section",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded phrase one", TextType.BOLD),
                TextNode(" section and ", TextType.TEXT),
                TextNode("bolded phrase two", TextType.BOLD),
                TextNode(" section", TextType.TEXT),
            ],
        )

    def test_split_italic_block(self):
        node = TextNode("This is text with a _italic phrase_ section", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic phrase", TextType.ITALIC),
                TextNode(" section", TextType.TEXT),
            ],
        )

    def test_split_double_italic_block(self):
        node = TextNode(
            "This is text with a _italic one_ section and _italic two_ section",
            TextType.TEXT,
        )
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic one", TextType.ITALIC),
                TextNode(" section and ", TextType.TEXT),
                TextNode("italic two", TextType.ITALIC),
                TextNode(" section", TextType.TEXT),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_delimiter_not_found(self):
        node = TextNode("This is text with a **italic phrase_ section", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/abcdefg.png) and ![image3](https://i.imgur.com/zxcvbn.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image2", "https://i.imgur.com/abcdefg.png"),
                ("image3", "https://i.imgur.com/zxcvbn.png"),
            ],
            matches,
        )

    def test_no_images(self):
        matches = extract_markdown_images("This is text with no image")
        self.assertListEqual([], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_link(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_multiple_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and [to discord](https://discord.com/invite/bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
                ("to discord", "https://discord.com/invite/bootdotdev"),
            ],
            matches,
        )

    def test_no_links(self):
        matches = extract_markdown_links("This is text with no links")
        self.assertListEqual([], matches)


class TestSplitNodesLinks(unittest.TestCase):
    def test_single_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
        )

    def test_single_link_with_closing_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and some random closing statement",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and some random closing statement", TextType.TEXT),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and [to discord](https://discord.com/invite/bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to discord", TextType.LINK, "https://discord.com/invite/bootdotdev"
                ),
            ],
        )

    def test_multiple_links_with_closing_text(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) and [to discord](https://discord.com/invite/bootdotdev) and some random closing statement",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to discord", TextType.LINK, "https://discord.com/invite/bootdotdev"
                ),
                TextNode(" and some random closing statement", TextType.TEXT),
            ],
        )

    def test_no_link(self):
        node = TextNode(
            "This is text with no links",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no links", TextType.TEXT),
            ],
        )

    def test_link_with_image(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(
                    " and an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT
                ),
            ],
        )

    def test_only_link(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ],
        )


class TestSplitNodesImages(unittest.TestCase):
    def test_single_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )

    def test_single_image_with_closing_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and random closing statement",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and random closing statement", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and another ![third image](https://i.imgur.com/abcdefg.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/abcdefg.png"
                ),
            ],
            new_nodes,
        )

    def test_multiple_images_with_closing_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and another ![third image](https://i.imgur.com/abcdefg.png) and with some random closing statement",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "third image", TextType.IMAGE, "https://i.imgur.com/abcdefg.png"
                ),
                TextNode(" and with some random closing statement", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_no_image(self):
        node = TextNode(
            "This is text with no images",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with no images", TextType.TEXT),
            ],
        )

    def test_image_with_link(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(
                    " and a link [to boot dev](https://www.boot.dev)", TextType.TEXT
                ),
            ],
        )

    def test_only_image(self):
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
        )


if __name__ == "__main__":
    unittest.main()
