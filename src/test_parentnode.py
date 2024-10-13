import unittest
from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_values(self):
        node = ParentNode(
            "div",
            [],
            {"href": "https://www.google.com"},
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.children,
            [],
        )
        self.assertEqual(
            node.props,
            {"href": "https://www.google.com"},
        )

    def test_repr(self):
        node = ParentNode(
            "a",
            [LeafNode(None, "Hi", None)],
            {"href": "https://www.google.com"},
        )
        self.assertEqual(
            repr(node),
            "ParentNode(a, [LeafNode(None, Hi, None)], {'href': 'https://www.google.com'})",
        )

    def test_to_html(self):
        node = ParentNode(None, [], None)
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode("a", None, None)
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode("a", [], None)
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode("a", [LeafNode(None, "Hi", None)], None)
        self.assertEqual(node.to_html(), "<a>Hi</a>")

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

        node = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>",
        )


if __name__ == "__main__":
    unittest.main()
