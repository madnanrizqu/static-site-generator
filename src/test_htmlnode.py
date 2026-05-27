import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
    def test_basic_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_no_tag_to_html_p(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_complete_to_html_button(self):
        node = LeafNode(
            "button",
            "Lorem ipsum color damet",
            None,
            {"style": "background-color: black; color: red; font-size: 24px"},
        )

        self.assertEqual(
            node.to_html(),
            '<button style="background-color: black; color: red; font-size: 24px">Lorem ipsum color damet</button>',
        )

    def test_repr(self):
        node = LeafNode(
            "button",
            "Lorem ipsum color damet",
            None,
            {"style": "background-color: black; color: red; font-size: 24px"},
        )

        self.assertEqual(
            repr(node),
            "LeafNode(button, Lorem ipsum color damet, children: None, {'style': 'background-color: black; color: red; font-size: 24px'})",
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>"
        )

    def test_to_html_with_children_no_tag_leaf(self):
        child_node = LeafNode("span", "child")
        child_node1 = LeafNode(None, "child no tag")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode(None, "child no tag 2")
        parent_node = ParentNode(
            "div", [child_node, child_node1, child_node2, child_node3]
        )
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>child</span>child no tag<b>child2</b>child no tag 2</div>",
        )

    def test_to_html_with_props(self):
        child_prop = {"style": "background-color: white; color: blue; font-size: 20px"}
        child_node = LeafNode("span", "child", None, child_prop)
        parent_prop = {"style": "background-color: black; color: red; font-size: 24px"}
        parent_node = ParentNode("div", [child_node], parent_prop)
        self.assertEqual(
            parent_node.to_html(),
            '<div style="background-color: black; color: red; font-size: 24px"><span style="background-color: white; color: blue; font-size: 20px">child</span></div>',
        )

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        with self.assertRaises(ValueError):
            ParentNode(None, [child_node]).to_html()

    def test_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            repr(parent_node),
            "ParentNode(div, children: [LeafNode(span, child, children: None, None)], None)",
        )


if __name__ == "__main__":
    unittest.main()
