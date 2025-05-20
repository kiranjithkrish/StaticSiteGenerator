import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, split_nodes_images, split_nodes_links, text_to_textnodes

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_notEq(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another node", TextType.BOLD)
        self.assertNotEqual(node1, node2)
    
    def test_notEq_forDifferentTextType(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another node", TextType.CODE)
        self.assertNotEqual(node1, node2)
        
    def test_urlIsNone(self):
        node1 = TextNode("This is a text node", TextType.BOLD)
        self.assertIsNone(node1.url)  
        
    def test_urlIsNotNone(self):
        node1 = TextNode("This is a text node", TextType.BOLD, url="kindered.com")
        self.assertIsNotNone(node1.url)
    
    def test_text_node_to_html_node_for_text_type(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        
    def test_text_node_to_html_node_for_Image_type(self):
        node = TextNode("An unknown image", TextType.IMAGE, "https://www.image.com")  
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"https://www.image.com", "alt":"An unknown image"})
        
    def test_text_node_to_html_node_for_Anchor_type(self):
        node = TextNode("Link description", TextType.LINK, "https://www.image.com")  
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link description")
        self.assertEqual(html_node.props, {"href":"https://www.image.com"})
    
    def test_text_node_to_html_node_for_Unknown_type(self):
        node = TextNode("Text description", "UNKNOWN") 
        with self.assertRaises(Exception):
             html_node = text_node_to_html_node(node)
             
    def test_split_nodes_with_delimiter_returns_new_nodes(self):
        node1 = TextNode("This is a **bold** text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        expected = [ TextNode("This is a ", TextType.NORMAL),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" text node", TextType.NORMAL)
                    ]
        self.assertEqual(len(new_nodes), len(expected))
        for i, (res_node, exp_node) in enumerate(zip(new_nodes, expected)):
            assert res_node.text == exp_node.text
            assert res_node.text_type == exp_node.text_type
            
    def test_splitNodesWithDelimiter_whenDelimterNotPresent_returnsEmptyNodes(self):
        node1 = TextNode("This is a bold text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        expected = [TextNode("This is a bold text node", TextType.NORMAL)]
        self.assertEqual(len(new_nodes), len(expected))
        
    def test_splitNodesWithDelimiter_whenTextNodesEmpty_returnsEmptyNodes(self):
        new_nodes = split_nodes_delimiter([], "**", TextType.BOLD)
        expected = []
        self.assertEqual(len(new_nodes), len(expected))
    
    def test_splitNodesWithDelimiter_whenDelimiterIsUnbalanced_throwsException(self):
        node1 = TextNode("This is a **bold** **text node", TextType.NORMAL)
        with self.assertRaises(Exception) as context:
            new_nodes = split_nodes_delimiter([node1], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), 'Unbalanced delimiter **')
        
    def test_split_nodes_with_delimiter_whenMultipleInputNodes_returns_new_nodes(self):
        node1 = TextNode("This is a **bold** text node", TextType.NORMAL)
        node2 = TextNode("This is another **code** text node", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)
        expected = [ TextNode("This is a ", TextType.NORMAL),
                    TextNode("bold", TextType.BOLD),
                    TextNode(" text node", TextType.NORMAL),
                    TextNode("This is another ", TextType.NORMAL),
                    TextNode("code", TextType.BOLD),
                    TextNode(" text node", TextType.NORMAL)
                    ]
        self.assertEqual(len(new_nodes), len(expected))
        for i, (res_node, exp_node) in enumerate(zip(new_nodes, expected)):
            assert res_node.text == exp_node.text
            assert res_node.text_type == exp_node.text_type
            
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_when_type_is_not_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.IMAGE,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.IMAGE,)
            ],
            new_nodes,
        )
        
    def test_split_links(self):
        node = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        node2 = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node, node2])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_links_with_image(self):
        node2 = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_links([node2])
        self.assertListEqual(
            [
                TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
            ],
            new_nodes,
        )
    def test_split_images_with_links(self):
        node2 = TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node2])
        self.assertListEqual(
            [
                TextNode(
            "This is text with an [image](https://i.imgur.com/zjjcJKZ.png) and another [second image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
            ],
            new_nodes,
        )
    
    def test_split_images_with_link_and_image(self):
        node2 = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/3elNhQu.png)",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_images([node2])
        self.assertListEqual(
            [
        TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another ",
            TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png" )
            ],
            new_nodes,
        )
        
    def test_split_images_with_separate_link_and_image_nodes(self):
        node2 = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another ",
            TextType.NORMAL)
        node3 =  TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png" )
        new_nodes = split_nodes_images([node2, node3])
        self.assertListEqual(
            [
        TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another ",
            TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png" )
            ],
            new_nodes,
        )
        
    def test_text_to_textnodes_when_given_text_returns_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
                        TextNode("This is ", TextType.NORMAL),
                        TextNode("text", TextType.BOLD),
                        TextNode(" with an ", TextType.NORMAL),
                        TextNode("italic", TextType.ITALIC),
                        TextNode(" word and a ", TextType.NORMAL),
                        TextNode("code block", TextType.CODE),
                        TextNode(" and an ", TextType.NORMAL),
                        TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                        TextNode(" and a ", TextType.NORMAL),
                        TextNode("link", TextType.LINK, "https://boot.dev"),
                    ]
        self.assertEqual(nodes, expected)
        
def test_splitNodesWithDelimiter_whenDelimiterIsUnbalanced_throwsException(self):
    node = TextNode("Hello ** world", TextType.NORMAL)
    delimiter = "**"
    with self.assertRaises(Exception) as context:
        split_nodes_delimiter([node], delimiter, TextType.BOLD)
    self.assertEqual(str(context.exception), f'Unbalanced delimiter {delimiter}')
    
if __name__ == "__main__":
    unittest.main()


