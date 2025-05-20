import unittest
from inline_markdown import *

class TestInlineMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_nested_images(self):
        markdown_text = "![image[and] more](https://i.imgur.com/zjjcJKZ.png)"
        matches = extract_markdown_images(markdown_text)
        # Check that only the inner image is extracted
        self.assertListEqual([("image[and] more", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_nested_links(self):
        matches = extract_markdown_links(
            "This is ![image more](https://i.imgur.com/zjjcJKZ.png) text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_title(self):
        md = """# Title
    1. First item
    2. Second item with _italic_
    3. Third item
    """
        self.assertEqual(extract_title(md), "Title")

if __name__ == "__main__":
    unittest.main()