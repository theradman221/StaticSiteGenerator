import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from main import text_node_to_html_node

class TestTextNode(unittest.TestCase):
    def test_create(self):
        node = HTMLNode()
        self.assertTrue(node.children == None and node.props == None and node.tag == None and node.value == None)
    
    def test_props_to_html(self):
        node = HTMLNode(props={"Key":"Value"})
        string = node.props_to_html()
        self.assertEqual(string, " Key=\"Value\"")

    def test_props_to_html2(self):
        node = HTMLNode(props={"href": "not a website LOL!", "TEST": "VALUES!"})
        string = node.props_to_html()
        self.assertEqual(string, " href=\"not a website LOL!\" TEST=\"VALUES!\"")

    def test_create_assign(self):
        node = HTMLNode()
        node.tag = "test"
        self.assertTrue(node.tag == "test")

    def test_print(self):
        node = HTMLNode()
        self.assertEqual(str(node), "HTMLNode Tag: None, Value: None, Children: None, Props: None")

    # Tests related to LeafNode
    def test_creation(self):
        node = LeafNode(value = "a")
        self.assertEqual(node.value, "a")

    def test_bad_type(self):
        with self.assertRaises(ValueError):
            node = LeafNode(value = "A")
            node.value = None
            node.to_html()

    def test_to_html(self):
        node = LeafNode(tag = "A", value = "This is a paragraph of text")
        string = node.to_html()
        self.assertEqual(string, "<A>This is a paragraph of text</A>")

    def test_to_html2(self):
        node = LeafNode("A", "Click the link", {"href": "Zoobies are awesome.com!"})
        string = node.to_html()
        self.assertEqual(string, "<A href=\"Zoobies are awesome.com!\">Click the link</A>")

    # Tests related to ParentNodes
    # Tests with no props
    def test_creation(self):
        node = ParentNode(tag = "TEST", children= [LeafNode(tag = "Leaf1", value = "Leaf 1 Value", props = None)])
        expected_html = "<TEST><Leaf1>Leaf 1 Value</Leaf1></TEST>"
        self.assertEqual(expected_html, node.to_html())
        node.tag = None
        with self.assertRaises(ValueError):
            node.to_html()
        self.assertEqual(None, node.tag)
        node.tag = "ABC"
        node.children = []
        with self.assertRaises(ValueError):
            node.to_html()
        self.assertEqual("", node.props_to_html())

    # Tests with a prop(s)
    def test_creation_2(self):
        node = ParentNode(tag = "TEST", children= [LeafNode(tag = "Leaf1", value = "Leaf 1 Value")], props = {"Key": "Value"})
        expected_html = "<TEST Key=\"Value\"><Leaf1>Leaf 1 Value</Leaf1></TEST>"
        self.assertEqual(expected_html, node.to_html())

    # Test creation of a ParentNode with Multiple Children, copied this example ParentNode from boot.dev to see if all tests are lining up
    def test_creation_3(self):
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)       
        expected_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected_html)
    
    # Test what happens when a ParentNode has other ParentNodes as children
    def test_creation_4(self):
        node = ParentNode("OUTMOST", children = [], props = {"href" : "youtube.com", "Breakfast": "Waffles"})
        # Create more Children in this parent, after verifying that the .to_html fails properly with no children
        with self.assertRaises(ValueError):
            node.to_html()
        leaf1 = LeafNode("Leaf1", "Leaf 1 Value", {"href" : "fakewebsite.stl"})
        leaf2 = LeafNode("Leaf2", "Leaf 2 Value")
        leaf3 = LeafNode("idk", "sandwich")
        child1 = ParentNode("Parent1", [leaf1, leaf2], {"science" : "fishing"})
        child2 = ParentNode("Parent2", [leaf2], None)
        # Append child1, child2, and leaf3 to the outmost parent's children list
        node.children.append(child1)
        node.children.append(child2)
        node.children.append(leaf3)
        expected_html = "<OUTMOST href=\"youtube.com\" Breakfast=\"Waffles\"><Parent1 science=\"fishing\"><Leaf1 href=\"fakewebsite.stl\">Leaf 1 Value</Leaf1><Leaf2>Leaf 2 Value</Leaf2></Parent1><Parent2><Leaf2>Leaf 2 Value</Leaf2></Parent2><idk>sandwich</idk></OUTMOST>"
        self.assertEqual(node.to_html(), expected_html)

    # Test the main.py text_node_to_html_node function
    def test_text_to_html(self):
        # Create the TextNodes for testing
        text_normal = TextNode("normal", TextType.NORMAL, "This is junk, it shouldn't show up anywhere: normal")
        text_bold = TextNode("bold", TextType.BOLD, "This is junk, it shouldn't show up anywhere: bold")
        text_italic = TextNode("italic", TextType.ITALIC, "This is junk, it shouldn't show up anywhere: italic")
        text_code = TextNode("code", TextType.CODE, "This is junk, it shouldn't show up anywhere: code")
        text_link = TextNode("link", TextType.LINK, "websitelink.com: link")
        text_image = TextNode("image", TextType.IMAGE, "websiteimage.com: image")
        # Convert to html_nodes for testing
        normal_html = text_node_to_html_node(text_normal)
        bold_html = text_node_to_html_node(text_bold)
        italic_html = text_node_to_html_node(text_italic)
        code_html = text_node_to_html_node(text_code)
        link_html = text_node_to_html_node(text_link)
        image_html = text_node_to_html_node(text_image)
        to_test = [normal_html, bold_html, italic_html, code_html, link_html, image_html]
        # Expected values for each value of the nodes, 0 = tag, 1 = value, 2 = children, 3 = props, matches key off of the value property of an htmlnode
        expected_values = {
            "normal" : [None, "normal", None, None],
            "bold" : ["b", "bold", None, None],
            "italic" : ["i", "italic", None, None],
            "code" : ["code", "code", None, None],
            "link" : ["a", "link", None, {"href" : "websitelink.com: link"}],
            "" : ["img", "", None, {"src": "websiteimage.com: image", "alt": "image"}]
        }

        for html_node in to_test:
            expected = expected_values[html_node.value]
            # Test the tag, value, children, and props fields
            self.assertEqual(html_node.tag, expected[0])
            self.assertEqual(html_node.value, expected[1])
            self.assertEqual(html_node.children, expected[2])
            self.assertEqual(html_node.props, expected[3])
            # Make sure that creating a new LeafNode with the expected data doesn't give a different result
            test_create_equal = LeafNode(expected[0], expected[1], expected[3])
            self.assertEqual(html_node.to_html(), test_create_equal.to_html())



        



if __name__ == "__main__":
    unittest.main()