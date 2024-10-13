import unittest
from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_values(self):
        node = LeafNode(
            "div", "I wish I could read", {"href": "https://www.google.com"}
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.props,
            {"href": "https://www.google.com"},
        )

    def test_repr(self):
        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"},
        )
        self.assertEqual(
            repr(node),
            "LeafNode(a, Click me!, {'href': 'https://www.google.com'})",
        )

    def test_to_html(self):
        node = LeafNode(None, "Hello")
        self.assertEqual(
            node.to_html(),
            "Hello",
        )

        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(
            node.to_html(),
            "<p>This is a paragraph of text.</p>",
        )

        node = LeafNode(
            "a",
            "Click me!",
            {"href": "https://www.google.com"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>',
        )


if __name__ == "__main__":
    unittest.main()
