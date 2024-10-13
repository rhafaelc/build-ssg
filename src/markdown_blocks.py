import re
from htmlnode import ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_blocks(markdown):
    sections = markdown.split("\n\n")
    sections = list(map(lambda x: x.strip(), sections))
    sections = list(filter(lambda x: x != "", sections))
    return sections


def block_to_block_type(block):
    res = re.findall(r"(#{1,6})\s+(.*)", block)
    if res:
        return "heading"
    res = re.findall(r"`{3}(.+?)`{3}", block, re.DOTALL)
    if res:
        return "code"
    res = re.findall(r">\s+(.*)", block)
    if res and len(res) == len(block.split("\n")):
        return "quote"
    res = re.findall(r"(\*|-)\s+(.*)", block)
    if res and len(res) == len(block.split("\n")):
        return "unordered_list"
    res = re.findall(r"([0-9]+)\.\s+(.*)", block)
    if res and len(res) == len(block.split("\n")):
        for i, (num, content) in enumerate(res):
            expected = i + 1
            actual = int(num)
            if expected != actual:
                return "paragraph"
        return "ordered_list"
    return "paragraph"


def block_to_node(block):
    block_type = block_to_block_type(block)

    if block_type == "heading":
        level = block.count("#")
        content = block.strip("# ").strip()
        return f"h{level}", content, None

    if block_type == "code":
        content = re.findall(r"```(.*?)```", block, re.DOTALL)[0]
        return "pre", f"<code>{content.strip()}</code>", None

    if block_type == "quote":
        content = block.strip("> ").strip()
        return "blockquote", content, None

    if block_type == "unordered_list":
        items = re.findall(r"(\*|-)\s+(.*)", block)
        list_items = "\n".join([f"<li>{item[1]}</li>" for item in items])
        return "ul", list_items, None

    if block_type == "ordered_list":
        items = re.findall(r"([0-9]+)\.\s+(.*)", block)
        list_items = "\n".join([f"<li>{item[1]}</li>" for item in items])
        return "ol", list_items, None

    if block_type == "paragraph":
        content = block.strip()
        return "p", content, None

    return "p", block, None


def markdown_to_html(markdown):
    blocks = markdown_to_blocks(markdown)
    res = []
    for block in blocks:
        tag, value, props = block_to_node(block)
        inline = text_to_textnodes(value)
        nodes = [text_node_to_html_node(node) for node in inline]
        res.append(ParentNode(tag, nodes, props))
    res = ParentNode("div", res)
    return res


def extract_title(markdown):
    root = markdown_to_html(markdown)
    for child in root.children:
        if child.tag == "h1":
            leaf = child.children[0]
            return leaf.value
    raise Exception("Must have a title")
