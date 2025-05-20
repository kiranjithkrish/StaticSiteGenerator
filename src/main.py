from textnode import TextNode, TextType
from markdown import markdown_to_html_node
from inline_markdown import extract_title

import os
import shutil
import sys

def main():
    setup_public()
            
def copy_directory(source, destination):
    contents = os.listdir(source)
    for content in contents:
        source_path = os.path.join(source, content)
        destination_path = os.path.join(destination, content)
        if os.path.isdir(source_path):
            os.makedirs(destination_path, exist_ok=True)
            print(f"Creating directory {destination_path}")
            copy_directory(source_path, destination_path)
        elif os.path.isfile(source_path):
            shutil.copy(source_path, destination_path)

def cleanup_public():
    public_path = "docs"
    rel_public_path = os.path.join(os.path.dirname(__file__), "..", public_path)
    abs_public_path = os.path.abspath(rel_public_path)
    if os.path.exists(abs_public_path):
        shutil.rmtree(abs_public_path)
    os.makedirs(abs_public_path, exist_ok=True)
    return abs_public_path
               
def setup_public():            
    abs_public_path = cleanup_public()
    static_path = "static"
    rel_static_path = os.path.join(os.path.dirname(__file__), "..", static_path)
    abs_static_path = os.path.abspath(rel_static_path)
    if os.path.exists(abs_static_path):
        copy_directory(abs_static_path, abs_public_path)
    else:
        raise Exception('Set up the static folder')
    
    markdown_path = "content"
    rel_markdown_path = os.path.join(os.path.dirname(__file__), "..", markdown_path)
    abs_markdown_path = os.path.abspath(rel_markdown_path)
    
    template_path = "template.html"
    rel_template_path = os.path.join(os.path.dirname(__file__), "..", template_path)
    abs_template_path = os.path.abspath(rel_template_path)
    
    dest_path = "docs"
    rel_dest_path = os.path.join(os.path.dirname(__file__), "..", dest_path)
    abs_dest_path = os.path.abspath(rel_dest_path)
    
    args = sys.argv

    basepath = "/"
    if len(args) > 1:
        basepath = f"{args[1]}"
    generate_pages_recursive(markdown_path, template_path, dest_path, basepath)

def read_file(path):
        with open(path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content

                
def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    template = read_file(template_path)
    markdown = read_file(from_path)
    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)
    final_html = template.replace('{{ Title }}', title)
    final_html = final_html.replace('{{ Content }}', html)
    if basepath != "/":
        final_html = final_html.replace('href="/', f'href="{basepath}')
        final_html = final_html.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True) 
    with open(dest_path, 'w', encoding='utf-8') as file:
        file.write(final_html)
   
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    def crawl_directory(dir_path_content, dest_dir_path):
        markdown_paths = []
        contents = os.listdir(dir_path_content)
        for content in contents:
            source_path = os.path.join(dir_path_content, content)
            if not os.path.isdir(source_path):
                rel_markdown_path = os.path.join(os.path.dirname(__file__), "..", source_path)
                abs_markdown_path = os.path.abspath(rel_markdown_path)
                destination_file = content[:-2]+"html"
                dest_path = os.path.join(dest_dir_path, destination_file)
                rel_html_path = os.path.join(os.path.dirname(__file__), "..", dest_path)
                abs_html_path = os.path.abspath(rel_html_path)
                markdown_paths.append((abs_markdown_path, dest_path))
            else:
                dest_path = os.path.join(dest_dir_path, content)
                paths = crawl_directory(source_path, dest_path)
                markdown_paths.extend(paths)
        return markdown_paths
    all_paths = crawl_directory(dir_path_content, dest_dir_path)
    for tuple in all_paths:
        generate_page(tuple[0], template_path, tuple[1], basepath)
        

            

if __name__ == "__main__":
    main()
