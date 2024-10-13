import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

import unittest
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)


class TestSplitDelimiter(unittest.TestCase):
    def test_split(self):
        node = TextNode("This is text with a `code block` word", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
        )

        node = TextNode(
            "This is text with a **bolded phrase** in the middle", text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("bolded phrase", "bold"),
                TextNode(" in the middle", "text"),
            ],
        )

    def test_split_not_text(self):
        node1 = TextNode("This is text with a `code block` word `oi` s", text_type_text)
        node2 = TextNode("lulza", text_type_code)
        new_nodes = split_nodes_delimiter([node1, node2], "`", text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word ", text_type_text),
                TextNode("oi", text_type_code),
                TextNode(" s", text_type_text),
                TextNode("lulza", text_type_code),
            ],
        )

    # def test_split_err(self):
    #     node = TextNode("This is text with a `code block` word `oi` s", text_type_text)
    #     self.assertRaises(Exception, split_nodes_delimiter, [node], "*", text_type_code)

    def test_multiple_split(self):
        node = TextNode("This is text with a `code block` word `oi` s", text_type_text)
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word ", text_type_text),
                TextNode("oi", text_type_code),
                TextNode(" s", text_type_text),
            ],
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", text_type_text)
        new_nodes = split_nodes_delimiter([node], "**", text_type_bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", text_type_italic)
        self.assertListEqual(
            [
                TextNode("bold", text_type_bold),
                TextNode(" and ", text_type_text),
                TextNode("italic", text_type_italic),
            ],
            new_nodes,
        )


class TestExtractMarkdownImages(unittest.TestCase):

    def test_single_match(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        res = extract_markdown_images(text)
        self.assertEqual(
            res,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ],
        )

    def test_multiple_match(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = extract_markdown_images(text)
        self.assertEqual(
            res,
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
        )

    def test_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        res = extract_markdown_images(text)
        self.assertEqual(
            res,
            [],
        )


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_single_match(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        res = extract_markdown_links(text)
        self.assertEqual(
            res,
            [
                ("to boot dev", "https://www.boot.dev"),
            ],
        )

    def test_multiple_match(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        res = extract_markdown_links(text)
        self.assertEqual(
            res,
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
        )

    def test_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        res = extract_markdown_links(text)
        self.assertEqual(
            res,
            [],
        )


class TestSplitNodeImage(unittest.TestCase):
    def test_single(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_multiple(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node, node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_image, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_with_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
                    text_type_text,
                ),
            ],
        )

    def test_image_with_link(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_image, "https://www.boot.dev"),
                TextNode(
                    " and [to youtube](https://www.youtube.com/@bootdotdev)",
                    text_type_text,
                ),
            ],
        )


class TestSplitNodeLinks(unittest.TestCase):
    def test_single(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_multiple(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node, node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(" and ", text_type_text),
                TextNode(
                    "to youtube", text_type_link, "https://www.youtube.com/@bootdotdev"
                ),
            ],
        )

    def test_with_image(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode(
                    "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
                    text_type_text,
                ),
            ],
        )

    def test_link_with_image(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)",
            text_type_text,
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", text_type_text),
                TextNode("to boot dev", text_type_link, "https://www.boot.dev"),
                TextNode(
                    " and ![to youtube](https://www.youtube.com/@bootdotdev)",
                    text_type_text,
                ),
            ],
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_empty(self):
        text = ""
        res = text_to_textnodes(text=text)
        exp = []
        self.assertEqual(res, exp)

    def test_only_text(self):
        text = "This is "
        res = text_to_textnodes(text=text)
        exp = [
            TextNode("This is ", text_type_text),
        ]
        self.assertEqual(res, exp)

    def test_only_bold(self):
        text = "**This is **"
        res = text_to_textnodes(text=text)
        exp = [
            TextNode("This is ", text_type_bold),
        ]
        self.assertEqual(res, exp)

    def test_only_italic(self):
        text = "*This is *"
        res = text_to_textnodes(text=text)
        exp = [
            TextNode("This is ", text_type_italic),
        ]
        self.assertEqual(res, exp)

    def test_only_code(self):
        text = "`This is `"
        res = text_to_textnodes(text=text)
        exp = [
            TextNode("This is ", text_type_code),
        ]
        self.assertEqual(res, exp)

    def test_only_image(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = text_to_textnodes(text=text)
        exp = [
            TextNode(
                "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertEqual(res, exp)

    def test_only_link(self):
        text = "[obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        res = text_to_textnodes(text=text)
        exp = [
            TextNode(
                "obi wan image", text_type_link, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertEqual(res, exp)

    def test_all_types(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        res = text_to_textnodes(text=text)
        exp = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode(
                "obi wan image", text_type_image, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertEqual(res, exp)


if __name__ == "__main__":
    unittest.main()
