import unittest
import textwrap
from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_to_node,
    markdown_to_html,
    extract_title,
)
from htmlnode import ParentNode, LeafNode


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = textwrap.dedent(
            """
            # Hello
            """
        )
        exp = "Hello"
        self.assertEqual(extract_title(markdown), exp)

    def test_extract_title_err(self):
        markdown = textwrap.dedent(
            """
            ## Hello
            """
        )
        self.assertRaises(Exception, extract_title, markdown)


class TestBlockToNode(unittest.TestCase):
    def test_block_to_node(self):
        test_cases = [
            {
                "block": "# Heading 1",
                "expected_tag": "h1",
                "expected_value": "Heading 1",
                "expected_props": None,
            },
            {
                "block": "## Heading 2",
                "expected_tag": "h2",
                "expected_value": "Heading 2",
                "expected_props": None,
            },
            {
                "block": "### Heading 3",
                "expected_tag": "h3",
                "expected_value": "Heading 3",
                "expected_props": None,
            },
            {
                "block": "#### Heading 4",
                "expected_tag": "h4",
                "expected_value": "Heading 4",
                "expected_props": None,
            },
            {
                "block": "##### Heading 5",
                "expected_tag": "h5",
                "expected_value": "Heading 5",
                "expected_props": None,
            },
            {
                "block": "###### Heading 6",
                "expected_tag": "h6",
                "expected_value": "Heading 6",
                "expected_props": None,
            },
            {
                "block": "```print('Hello World')```",
                "expected_tag": "pre",
                "expected_value": "<code>print('Hello World')</code>",
                "expected_props": None,
            },
            {
                "block": "> This is a quote",
                "expected_tag": "blockquote",
                "expected_value": "This is a quote",
                "expected_props": None,
            },
            {
                "block": textwrap.dedent(
                    """
                        * Item 1
                        * Item 2
                        * Item 3
                        """
                ).strip(),
                "expected_tag": "ul",
                "expected_value": "<li>Item 1</li>\n<li>Item 2</li>\n<li>Item 3</li>",
                "expected_props": None,
            },
            {
                "block": textwrap.dedent(
                    """
                        1. First
                        2. Second
                        3. Third
                    """
                ).strip(),
                "expected_tag": "ol",
                "expected_value": "<li>First</li>\n<li>Second</li>\n<li>Third</li>",
                "expected_props": None,
            },
            {
                "block": "This is a paragraph.",
                "expected_tag": "p",
                "expected_value": "This is a paragraph.",
                "expected_props": None,
            },
        ]

        for test_case in test_cases:
            with self.subTest(block=test_case["block"]):
                tag, value, props = block_to_node(test_case["block"])
                self.assertEqual(tag, test_case["expected_tag"])
                self.assertEqual(value, test_case["expected_value"])
                self.assertEqual(props, test_case["expected_props"])


class TestMarkdownToHtmlTableDriven(unittest.TestCase):
    def test_markdown_to_html(self):
        # Table-driven test cases
        test_cases = [
            {
                "name": "Heading and paragraph",
                "markdown": textwrap.dedent(
                    """
                    # Heading 1


                    This is a paragraph under the heading.
                    """
                ).strip(),
                "expected_structure": [
                    {"tag": "h1", "children": [LeafNode(None, "Heading 1")]},
                    {
                        "tag": "p",
                        "children": [
                            LeafNode(None, "This is a paragraph under the heading.")
                        ],
                    },
                ],
            },
            {
                "name": "Blockquote and paragraph",
                "markdown": textwrap.dedent(
                    """
                    > This is a blockquote.


                    This is a paragraph after the blockquote.
                    """
                ).strip(),
                "expected_structure": [
                    {
                        "tag": "blockquote",
                        "children": [LeafNode(None, "This is a blockquote.")],
                    },
                    {
                        "tag": "p",
                        "children": [
                            LeafNode(None, "This is a paragraph after the blockquote.")
                        ],
                    },
                ],
            },
            {
                "name": "Heading, unordered list, and paragraph",
                "markdown": textwrap.dedent(
                    """
                    ## Shopping List


                    * Apples
                    * Oranges
                    * Bananas


                    This is a paragraph after the list.
                    """
                ).strip(),
                "expected_structure": [
                    {"tag": "h2", "children": [LeafNode(None, "Shopping List")]},
                    {
                        "tag": "ul",
                        "children": [
                            LeafNode(
                                None,
                                "<li>Apples</li>\n<li>Oranges</li>\n<li>Bananas</li>",
                            )
                        ],
                    },
                    {
                        "tag": "p",
                        "children": [
                            LeafNode(None, "This is a paragraph after the list.")
                        ],
                    },
                ],
            },
        ]

        for case in test_cases:
            with self.subTest(case=case["name"]):
                html_node = markdown_to_html(case["markdown"])

                self.assertIsInstance(html_node, ParentNode)
                self.assertEqual(html_node.tag, "div")
                self.assertEqual(
                    len(html_node.children), len(case["expected_structure"])
                )

                for i, expected in enumerate(case["expected_structure"]):
                    child_node = html_node.children[i]
                    self.assertEqual(child_node.tag, expected["tag"])
                    for real, exp in zip(child_node.children, expected["children"]):
                        self.assertEqual(repr(real), repr(exp))


class TestMarkdownToBlocks(unittest.TestCase):
    def test_single(self):
        markdown = textwrap.dedent(
            """
            # Hi
            """
        )
        res = markdown_to_blocks(markdown)
        exp = ["# Hi"]
        self.assertEqual(res, exp)

    def test_none(self):
        markdown = textwrap.dedent(
            """
            """
        )
        res = markdown_to_blocks(markdown)
        exp = []
        self.assertEqual(res, exp)

    def test_multiple(self):
        markdown = textwrap.dedent(
            """
            # This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item
            """
        )

        res = markdown_to_blocks(markdown=markdown)
        exp = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            textwrap.dedent(
                """
                * This is the first list item in a list block
                * This is a list item
                * This is another list item
                """
            ).strip(),
        ]
        self.assertEqual(res, exp)

    def test_multiple_line(self):
        markdown = textwrap.dedent(
            """
            # This is a heading




            This is a paragraph of text. It has some **bold** and *italic* words inside of it.




            * This is the first list item in a list block
            * This is a list item
            * This is another list item
            """
        )

        res = markdown_to_blocks(markdown=markdown)
        exp = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            textwrap.dedent(
                """
                * This is the first list item in a list block
                * This is a list item
                * This is another list item
                """
            ).strip(),
        ]
        self.assertEqual(res, exp)


class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        block = "# Hi"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "###### Hi"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "######Hi"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_code(self):
        block = "```yohohoho```"
        self.assertEqual(block_to_block_type(block), "code")

        block = textwrap.dedent(
            """
            ```
            hahah
            ```
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "code")

        block = textwrap.dedent(
            """
            ```


            hahah


            ```
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "code")

        block = "```yohohoho``"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_quote(self):
        block = "> asdasd"
        self.assertEqual(block_to_block_type(block), "quote")

        block = textwrap.dedent(
            """
            > asdasd
            > adasd
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "quote")

        block = textwrap.dedent(
            """
            > asdasd
            asdasd
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_unordered_list(self):
        block = textwrap.dedent(
            """
            * This is the first list item in a list block
            * This is a list item
            * This is another list item
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "unordered_list")

        block = textwrap.dedent(
            """
            - This is the first list item in a list block
            - This is a list item
            - This is another list item
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "unordered_list")

        block = textwrap.dedent(
            """
            - This is the first list item in a list block
            * This is a list item
            - This is another list item
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "unordered_list")

        block = textwrap.dedent(
            """
            - This is the first list item in a list block
            * This is a list item
            This is another list item
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_ordered_list(self):
        block = textwrap.dedent(
            """
            1. This is the first list item in a list block
            2. This is a list item
            3. This is another list item
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "ordered_list")

        block = textwrap.dedent(
            """
            1. This is the first list item in a list block
            2. This is a list item
            4. This is another list item
            """
        ).strip()
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_paragraph(self):
        block = "ahahhaha"
        self.assertEqual(block_to_block_type(block), "paragraph")


if __name__ == "__main__":
    unittest.main()
