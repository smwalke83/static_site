from textmanipfunc import markdown_to_blocks, markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
import sys, os, shutil

def copy_to_directory(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
    if not os.path.exists(destination):
        os.mkdir(destination)
    items = os.listdir(source)
    for item in items:
        source_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            os.mkdir(dest_path)
            copy_to_directory(source_path, dest_path)
def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    header = None
    for block in blocks:
        if block.startswith("# "):
            header = block.lstrip("#").strip()
    if header == None:
        raise Exception("no title header")
    return header
def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = read_file_contents(from_path)
    template = read_file_contents(template_path)
    md_node = markdown_to_html_node(md)
    md_html = md_node.to_html()
    title = extract_title(md)
    new_template = template.replace("{{ Title }}", title).replace("{{ Content }}", md_html)
    basepath_template = new_template.replace('href="/', f'href="{basepath}').replace('src="/', f'src="{basepath}')
    directory, filename = get_directory_and_filename(dest_path)
    create_and_write_file(directory, filename, basepath_template)
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)
    items = os.listdir(dir_path_content)
    for item in items:
        content_path = os.path.join(dir_path_content, item)
        dest_path = os.path.join(dest_dir_path, item)
        if os.path.isfile(content_path):
            path = dest_path.split(".")[0] + ".html"
            generate_page(content_path, template_path, path, basepath)
        else:
            os.mkdir(dest_path)
            generate_pages_recursive(content_path, template_path, dest_path, basepath)
def create_and_write_file(directory, filename, content):
    os.makedirs(directory, exist_ok = True)
    filepath = os.path.join(directory, filename)
    file = open(filepath, "w")
    file.write(content)
    file.close
def get_directory_and_filename(filepath):
    list = filepath.split("/")
    filename = list[-1]
    directory = os.path.dirname(filepath)
    return directory, filename
def read_file_contents(filepath):
    file = open(filepath)
    content = file.read()
    file.close()
    return content
