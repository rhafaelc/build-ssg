from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            res.append(node)
            continue
        texts = node.text.split(delimiter)
        if len(texts) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        # if len(texts) == 1:
        #     raise Exception(f"{delimiter} was not found")
        for i in range(len(texts)):
            if texts[i] == "":
                continue
            if i % 2 == 0:
                res.append(TextNode(texts[i], text_type_text))
            else:
                res.append(TextNode(texts[i], text_type))
    return res


def extract_markdown_images(text):
    res = re.findall(r"\!\[(.*?)\]\((.*?)\)", text)
    return res


def extract_markdown_links(text):
    res = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return res


def split_nodes(old_nodes, image=None, link=None):
    if not image and not link:
        raise Exception("please pick image or link")
    res = []
    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            res.append(old_node)
            continue

        original_text = old_node.text
        sections = [original_text]
        while sections:
            text = sections[0]
            if text == "":
                break

            if link:
                alt_urls = extract_markdown_links(text)
                if not alt_urls:
                    res.append(TextNode(text, text_type_text))
                    break
                alt, url = alt_urls[0]
                tmp = text.split(f"[{alt}]({url})", 1)
            if image:
                alt_urls = extract_markdown_images(text)
                if not alt_urls:
                    res.append(TextNode(text, text_type_text))
                    break
                alt, url = alt_urls[0]
                tmp = text.split(f"![{alt}]({url})", 1)
            res.append(TextNode(tmp[0], text_type_text))
            if image:
                res.append(TextNode(alt, text_type_image, url))
            if link:
                res.append(TextNode(alt, text_type_link, url))
            sections = [tmp[1]]

    return [r for r in res if r.text != ""]


def split_nodes_image(old_nodes):
    return split_nodes(old_nodes=old_nodes, image=True)


def split_nodes_link(old_nodes):
    return split_nodes(old_nodes=old_nodes, link=True)


def text_to_textnodes(text):
    node = TextNode(text, text_type_text)
    res = [node]
    res = split_nodes_delimiter(res, "**", text_type_bold)
    res = split_nodes_delimiter(res, "*", text_type_italic)
    res = split_nodes_delimiter(res, "`", text_type_code)
    res = split_nodes_image(res)
    res = split_nodes_link(res)
    return res
