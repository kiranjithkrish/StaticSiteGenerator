import unittest
from blocks import markdown_to_blocks, block_to_block_type, BlockType

class Test_Blocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_with_spaces_to_blocks(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line

            - This is a list
            - with items    
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_with_extra_spaces_to_blocks(self):
        md = """
            This is **bolded** paragraph


            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line


            - This is a list
            - with items    
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_with_no_spaces_to_blocks(self):
        md = """
            This is **bolded** paragraph
            This is another paragraph with _italic_ text and `code` here
            This is the same paragraph on a new line
            - This is a list
            - with items    
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph\nThis is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line\n- This is a list\n- with items",
            ],
        )
        
    def test_empty_markdown_to_blocks(self):
        md = """
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            []
        )
        
    def test_block_to_block_type_valid_input(self):
        ordered_list_test = """1. First item
2. Second item
3. Third item"""

        result = block_to_block_type(ordered_list_test)
        self.assertEqual(result, BlockType.ORDERED_LIST)    
        
    def test_block_to_block_type_invalid_input(self):
        ordered_list_test = """1. First item
1. Second item
3. Third item"""

        result = block_to_block_type(ordered_list_test)
        self.assertEqual(result, BlockType.PARAGRAPH) 
        
    
    def test_block_to_block_type_ordered_list_with_wrong_intendation_gives_paragraph(self):
        ordered_list_test = """1. First item
    2. Second item
    3. Third item"""

        result = block_to_block_type(ordered_list_test)
        self.assertEqual(result, BlockType.PARAGRAPH)     
    
    def test_block_to_block_type_given_a_block_returns_the_type(self):
        test_blocks = [
    # Paragraph
    "This is a normal paragraph with no special formatting.\nIt can span multiple lines and doesn't match any other block type.",
    
    # Headings
    "# Heading level 1",
    "## Heading level 2",
    "### Heading level 3",
    "#### Heading level 4",
    "##### Heading level 5",
    "###### Heading level 6",
    
    # Code Block
    "```\ndef hello_world():\n    print(\"Hello, world!\")\n```",
    
    # Quote Block
    "> This is a quote block.\n> Each line starts with a greater-than symbol.\n> This is the third line of the quote.",
    
    # Unordered List
    "- This is the first item\n- This is the second item\n- This is the third item",
    
    # Ordered List
    "1. This is the first item\n2. This is the second item\n3. This is the third item",
    
    # Edge Cases
    "#No space after hash",
    "-No space after dash",
    "1.No space after period",
    "> First line is quote\nSecond line isn't",
    "1. First item\n3. Third item"
]
        expected_outputs = [
    # Paragraph
    BlockType.PARAGRAPH,
    
    # Headings
    BlockType.HEADING,
    BlockType.HEADING,
    BlockType.HEADING,
    BlockType.HEADING,
    BlockType.HEADING,
    BlockType.HEADING,
    
    # Code Block
    BlockType.CODE,
    
    # Quote Block
    BlockType.QUOTE,
    
    # Unordered List
    BlockType.UNORDERED_LIST,
    
    # Ordered List
    BlockType.ORDERED_LIST,
    
    # Edge Cases (all should be paragraphs according to the requirements)
    BlockType.PARAGRAPH,  # #No space after hash
    BlockType.PARAGRAPH,  # -No space after dash
    BlockType.PARAGRAPH,  # 1.No space after period
    BlockType.PARAGRAPH,  # > First line is quote\nSecond line isn't
    BlockType.PARAGRAPH   # 1. First item\n3. Third item (incorrect numbering)
]
        res_blocks = list(map(block_to_block_type, test_blocks))
        self.assertEqual(res_blocks, expected_outputs)
        
        