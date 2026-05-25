import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "Click here",
            None,
            {"href": "https://www.boot.dev", "target": "_blank"},
        )

        self.assertEqual(
            node.props_to_html(), ' href="https://www.boot.dev" target="_blank"'
        )

    def test_empty_props_to_html(self):
        node = HTMLNode(
            "div",
            "Boot dev is a gem",
        )

        self.assertEqual(node.props_to_html(), "")

    def test_values(self):
        node = HTMLNode(
            "div",
            "Boot dev is a gem",
        )

        self.assertEqual(node.tag, "div")

        self.assertEqual(node.value, "Boot dev is a gem")

        self.assertEqual(node.children, None)

        self.assertEqual(node.props, None)

    def test_repr(self):
        child_node = HTMLNode("span", "sitta")
        child_node2 = HTMLNode("span", "lemma")
        node = HTMLNode(
            "p",
            "Lorem ipsum color damet",
            [child_node, child_node2],
            {"style": "background-color: black; color: red; font-size: 24px"},
        )

        self.assertEqual(
            repr(node),
            "HTMLNode(p, Lorem ipsum color damet, children: [HTMLNode(span, sitta, children: None, None), HTMLNode(span, lemma, children: None, None)], {'style': 'background-color: black; color: red; font-size: 24px'})",
        )


if __name__ == "__main__":
    unittest.main()
