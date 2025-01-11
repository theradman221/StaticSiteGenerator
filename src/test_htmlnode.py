import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

        



if __name__ == "__main__":
    unittest.main()