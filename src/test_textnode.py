import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
    text_node_to_html_node,
)
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq1(self):
        node1 = TextNode("This is a text node", text_type_bold)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertEqual(node1, node2)

    def test_eq2(self):
        node1 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertEqual(node1, node2)

    # diff 1
    def test_noteq1(self):
        node1 = TextNode("This is a text", text_type_bold, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_noteq2(self):
        node1 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_noteq3(self):
        node1 = TextNode("This is a text node", text_type_bold, "boot")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    # diff 2
    def test_noteq4(self):
        node1 = TextNode("This is a text node", text_type_italic, "boot")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_noteq5(self):
        node1 = TextNode("This is a text", text_type_bold, "boot")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_noteq6(self):
        node1 = TextNode("This is a text", text_type_italic, "https://www.boot.dev")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    # diff 3
    def test_noteq7(self):
        node1 = TextNode("This is a text", text_type_italic, "boot")
        node2 = TextNode("This is a text node", text_type_bold, "https://www.boot.dev")
        self.assertNotEqual(node1, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_text_node_to_html_node(self):
        node = TextNode("Hello", "tes")
        self.assertRaises(Exception, text_node_to_html_node, node)

        node = TextNode("Hello", text_type_text)
        self.assertEqual(
            repr(text_node_to_html_node(node)), repr(LeafNode(None, "Hello", None))
        )

        node = TextNode("Hello", text_type_bold)
        self.assertEqual(
            repr(text_node_to_html_node(node)), repr(LeafNode("b", "Hello", None))
        )

        node = TextNode("Hello", text_type_italic)
        self.assertEqual(
            repr(text_node_to_html_node(node)), repr(LeafNode("i", "Hello", None))
        )

        node = TextNode("Hello", text_type_code)
        self.assertEqual(
            repr(text_node_to_html_node(node)), repr(LeafNode("code", "Hello", None))
        )

        node = TextNode("Hello", text_type_link, "https://boot.dev")
        self.assertEqual(
            repr(text_node_to_html_node(node)),
            repr(LeafNode("a", "Hello", {"href": "https://boot.dev"})),
        )

        node = TextNode("Hello", text_type_image, "https://boot.dev")
        self.assertEqual(
            repr(text_node_to_html_node(node)),
            repr(LeafNode("img", None, {"src": "https://boot.dev", "alt": "Hello"})),
        )


if __name__ == "__main__":
    unittest.main()
