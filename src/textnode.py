from enum import Enum
from htmlnode import HTMLNode, LeafNode
from inline_markdown import extract_markdown_images, extract_markdown_links

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
                self.text == other.text 
                and self.text_type == other.text_type 
                and self.url == other.url
                )

    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type.value}, {self.url})'

def text_node_to_html_node(text_node):
    match (text_node.text_type):
        case TextType.NORMAL:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode("b", text_node.text, None)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text, None)
        case TextType.CODE:
            return LeafNode("code", text_node.text, None)
        case TextType.LINK:
            props = {"href": text_node.url}
            return LeafNode("a", text_node.text, props)
        case TextType.IMAGE:
            props = {"src": text_node.url, "alt": text_node.text}
            return LeafNode("img", "", props)
        case _:
            raise Exception()
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        components = node.text.split(delimiter)
        if len(components)%2 == 0:
            raise  Exception(f'Unbalanced delimiter {delimiter}')
        for i in range(len(components)):
            new_node = None
            if i % 2 != 0:
                new_node = TextNode(components[i], text_type)
            else:
                new_node = TextNode(components[i], TextType.NORMAL)
            new_nodes.append(new_node)
    return new_nodes

def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        image_markdown_list = extract_markdown_links(node.text)
        current_text = node.text
        if not image_markdown_list:
            new_nodes.append(node)
        else:
            for image_markdown in image_markdown_list:
                image_alt, image_link = image_markdown[0], image_markdown[1]
                
                components = current_text.split(f'[{image_alt}]({image_link})', 1)
                if components[0]:
                    new_nodes.append(TextNode(components[0], text_type=TextType.NORMAL))
                new_nodes.append(TextNode(image_alt, TextType.LINK, image_link))
                if len(components) > 1:
                    current_text = components[1]
                else:
                    current_text = ""
            if current_text:
                current_text_node = TextNode(current_text, TextType.NORMAL)
                new_nodes.append(current_text_node)
    return new_nodes
            
            
        
def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue
        image_markdown_list = extract_markdown_images(node.text)
        current_text = node.text
        if not image_markdown_list:
            new_nodes.append(node)
        else:
            for image_markdown in image_markdown_list:
                image_alt, image_link = image_markdown[0], image_markdown[1]
                
                components = current_text.split(f'![{image_alt}]({image_link})', 1)
                if components[0]:
                    new_nodes.append(TextNode(components[0], text_type=TextType.NORMAL))
                new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                if len(components) > 1:
                    current_text = components[1]
                else:
                    current_text = ""
            if current_text:
                current_text_node = TextNode(current_text, TextType.NORMAL)
                new_nodes.append(current_text_node)
    return new_nodes


def text_to_textnodes(text):
    text_node = [TextNode(text, TextType.NORMAL)]
    image_and_text = split_nodes_images(text_node)
    link_image_and_text = split_nodes_links(image_and_text)
    bold_link_image_and_text = split_nodes_delimiter(link_image_and_text, "**", TextType.BOLD)
    italic_bold_link_image_and_text = split_nodes_delimiter(bold_link_image_and_text, "_", TextType.ITALIC)
    code_italic_bold_link_image_and_text = split_nodes_delimiter(italic_bold_link_image_and_text, "`", TextType.CODE)
    return code_italic_bold_link_image_and_text

def text_to_children_html(text):
    text_nodes = text_to_textnodes(text)
    return list(map(text_node_to_html_node, text_nodes))
        
    
    
    
    
            
            
            