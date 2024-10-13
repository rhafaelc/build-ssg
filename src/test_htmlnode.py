import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html_exception(self):
        node = HTMLNode()
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        res = node.props_to_html()
        self.assertEqual(res, ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode()
        res = node.props_to_html()
        self.assertEqual(res, "")

    def test_repr(self):
        node = HTMLNode(
            "a", "Hello guys", HTMLNode(), {"href": "https://www.google.com"}
        )
        res = repr(node)
        self.assertEqual(
            res,
            "HTMLNode(a, Hello guys, HTMLNode(None, None, None, None), {'href': 'https://www.google.com'})",
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
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
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )


if __name__ == "__main__":
    unittest.main()
