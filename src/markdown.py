from textnode import TextNode, TextType, text_node_to_html_node, text_to_children_html
from blocks import markdown_to_blocks, block_to_block_type, BlockType, is_heading
from htmlnode import HTMLNode, ParentNode
    
def markdown_to_html_node(markdown):
    res_html_nodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        type = block_to_block_type(block)
        
        match (type):
            case BlockType.PARAGRAPH:
                cleaned_block = block.replace('\n', ' ')
                children_html = text_to_children_html(cleaned_block)
                p_node =  ParentNode("p",children=children_html)
                res_html_nodes.append(p_node)
            case BlockType.QUOTE:
                
                lines = block.split('\n')
                cleaned_lines = []
                for line in lines:
                    if line.startswith('> '):
                        cleaned_lines.append(line[2:])  # Remove '> '
                    elif line.startswith('>'):
                        cleaned_lines.append(line[1:])  # Remove '>'
                    else:
                        cleaned_lines.append(line)  # Keep as is (might be an empty line)
                cleaned_block = " ".join(cleaned_lines)
                html_nodes = text_to_children_html(cleaned_block)
                block_node =  ParentNode("blockquote", children=html_nodes)
                res_html_nodes.append(block_node)
            case BlockType.CODE:
                lines = block.split('\n')
                if lines and lines[0].strip().startswith('```'):
                    lines = lines[1:]
                if lines and lines[-1].strip().endswith('```'):
                    lines = lines[:-1]
                code = "\n".join(lines) + "\n"
                
                text_node = TextNode(code, TextType.NORMAL)
                text_to_html = text_node_to_html_node(text_node)
                
                code_node = ParentNode("code", children=[text_to_html])
                pre_node = ParentNode("pre", children=[code_node])
                res_html_nodes.append(pre_node)
            case BlockType.UNORDERED_LIST:
                
                lines = block.split('\n')
                list_nodes = []
                for line in lines:
                    if not line.strip():
                        continue
                    line_text = line[2:]
                    html_nodes = text_to_children_html(line_text)
                    li_node = ParentNode("li",html_nodes)
                    list_nodes.append(li_node)
        
                ul_node =  ParentNode("ul", list_nodes)
                res_html_nodes.append(ul_node)
            case BlockType.ORDERED_LIST:
                lines = block.split('\n')
                list_nodes = []
                for i,line in enumerate(lines):
                    if not line.strip():
                        continue
                    parts = line.split('. ', 1)
                    if len(parts) == 2:
                        line_text = parts[1]  # Get everything after the number and period
                        html_nodes = text_to_children_html(line_text)
                        li_node = ParentNode("li", html_nodes)
                        list_nodes.append(li_node)
                ol_node =  ParentNode("ol", list_nodes)
                res_html_nodes.append(ol_node)
            case BlockType.HEADING:
                _, heading_level = is_heading(block)
                cleaned_block = block[heading_level+1:]
                html_nodes = text_to_children_html(cleaned_block)
                h_node =  ParentNode(f'h{heading_level}', html_nodes)
                res_html_nodes.append(h_node)
            case _:
                children_html = text_to_children_html(block)
                p_node =  ParentNode("p", children_html)
                res_html_nodes.append(p_node)
    parent_div = ParentNode("div", res_html_nodes)
    return parent_div
