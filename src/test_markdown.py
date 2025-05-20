import unittest
from markdown import * 

class TestMarkdown(unittest.TestCase):
    
    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
        
    def test_quote_block(self):
        md = """
    > This is a quote
    > with multiple lines
    > in it
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with multiple lines in it</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
    * Item 1
    * Item 2
    * Item 3 with **bold** text
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1</li><li>Item 2</li><li>Item 3 with <b>bold</b> text</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
    1. First item
    2. Second item with _italic_
    3. Third item
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second item with <i>italic</i></li><li>Third item</li></ol></div>",
        )

    def test_heading(self):
        md = """
    # Main Heading

    ## Secondary Heading with `code`

    ### Third level
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Main Heading</h1><h2>Secondary Heading with <code>code</code></h2><h3>Third level</h3></div>",
        )
        
   

if __name__ == "__main__":
    unittest.main()