import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_init(self):
        node = HTMLNode("p", "This is a p tag")
        self.assertIsNotNone(node)
        
    def test_props_to_html_returns_attributes_string(self):
        node = HTMLNode(props={"href": "https://example.com", "target": "_blank"})
        expected = ' href="https://example.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)
        
    def test_to_html(self):
        node = HTMLNode("p", "This is a p tag")
        with self.assertRaises(NotImplementedError):
            node.to_html()
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_with_anchor_and_href(self):
        node = LeafNode("a", "Click me!", {"href":"https://www.google.com"})
        expected = '<a href="https://www.google.com">Click me!</a>'
        self.assertEqual(node.to_html(), expected)
        
    def test_to_html_with_children(self):
        leaf_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[leaf_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
        
    def test_to_html_with_children_with_props(self):
        leaf_node = LeafNode("span", "child")
        parent_node = ParentNode("a", [leaf_node],{"href":"https://google.com"})
        self.assertEqual(parent_node.to_html(), '<a href="https://google.com"><span>child</span></a>')
    
    def test_to_html_with_children_with_empty_props(self):
        leaf_node = LeafNode("span", "child")
        parent_node = ParentNode("a", [leaf_node],{})
        self.assertEqual(parent_node.to_html(), '<a><span>child</span></a>')
        
    def test_to_html_when_children_is_empty(self):
        parent_node = ParentNode("div", children=[])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "Empty children")
    
    def test_to_html_when_tag_is_empty(self):
        parent_node = ParentNode("", children=[])
        with self.assertRaises(ValueError):
            parent_node.to_html()
        
    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
        
    
    
