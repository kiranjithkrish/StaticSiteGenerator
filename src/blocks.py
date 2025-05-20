from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    
def iscodeblock(block):
    if block.startswith('```') and block.endswith('```'):
        return True
    return False    
    
def is_heading(block):
    if not block.startswith('#'):
        return (False,0)
    count = 0
    for c in block:
        if c == "#":
            count += 1
        else:
            break
    return (True, count) if count > 0 and count < 7 and count < len(block) and block[count] == ' ' else (False,0)

def isquoteblock(block):
    lines = block.split('\n')
    return all([line.startswith('>') for line in lines])

def isunorderedlist(block):
    lines = block.split('\n')
    return all([not line.strip() or line.strip().startswith(('- ', '* ', '+ ')) for line in lines])
    
def isorderedlist(block):
    lines = block.split('\n')
    for i,line in enumerate(lines):
       start = i + 1
       prefix = f'{start}. '
       if not line.startswith(prefix):
           return False
    return True
    
def block_to_block_type(block_text):
    if is_heading(block_text)[0]:
        return BlockType.HEADING
    elif iscodeblock(block_text):
        return BlockType.CODE
    elif isquoteblock(block_text):
        return BlockType.QUOTE
    elif isunorderedlist(block_text):
        return BlockType.UNORDERED_LIST
    elif isorderedlist(block_text):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_blocks(markdown):
    blocks = markdown.split('\n\n')
    stripped_blocks = [block.strip() for block in blocks if block.strip()]
    res = []
    for stripped_block in stripped_blocks:
        strip_again_list = stripped_block.split('\n')
        clean_line = [line.strip() for line in strip_again_list]
        res.append('\n'.join(clean_line))
    return res


        
    
    