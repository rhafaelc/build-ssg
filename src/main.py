from textnode import TextNode, text_type_bold
import os
import shutil
from markdown_blocks import extract_title, markdown_to_html


def copy_content(src, dst):
    if not os.path.exists(src):
        raise Exception(f"folder {src} not found")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for item in os.listdir(src):
        in_path = os.path.join(src, item)
        out_path = os.path.join(dst, item)
        if not os.path.isfile(in_path):
            copy_content(in_path, out_path)
        else:
            shutil.copy(in_path, out_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
        f.close()
    with open(template_path) as f:
        template = f.read()
        f.close()
    title = extract_title(markdown)
    html = markdown_to_html(markdown).to_html()

    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dirname = os.path.dirname(dest_path)
    if not os.path.exists(dirname):
        os.mkdir(dirname)

    with open(dest_path, "w") as f:
        f.write(template)
        f.close()


def generate_page_recursive(dir_path_content, template_path, dest_dir_path):
    for item in os.listdir(dir_path_content):
        in_path = os.path.join(dir_path_content, item)
        out_path = os.path.join(dest_dir_path, item)

        if os.path.isdir(in_path):
            generate_page_recursive(in_path, template_path, out_path)
        else:
            out_path = os.path.splitext(out_path)[0] + ".html"
            generate_page(in_path, template_path, out_path)


def main():
    shutil.rmtree("public")
    copy_content("static", "public")
    # generate_page("content/index.md", "template.html", "public/index.html")
    # generate_page(
    #     "content/majesty/index.md", "template.html", "public/majesty/index.html"
    # )
    generate_page_recursive("content", "template.html", "public")


main()
