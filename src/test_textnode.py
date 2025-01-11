import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = TextNode("this is a text node", TextType.IMAGE, "YAMSURL>CORN")
        node2 = TextNode("this is a text node", TextType.IMAGE, "YAMSURL>CORN")
        self.assertEqual(node, node2)


    def test_not_eq_text(self):
        node = TextNode("this is a text! node", TextType.IMAGE, "YAMSURL>CORN")
        node2 = TextNode("this is a text node", TextType.IMAGE, "YAMSURL>CORN")
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("this is a text node", TextType.IMAGE, "YAMSURL>CORN")
        node2 = TextNode("this is a text node", TextType.IMAGE, "YAMSURL>CORN")
        # Test that if a variable is updated that __eq__ doesn't keep returning True
        node.url = "TESTING MODE"
        self.assertNotEqual(node, node2)
    
    def test_bad_type(self):
        with self.assertRaises(AttributeError):
            node = TextNode("Test Node", TextType.bald)


if __name__ == "__main__":
    unittest.main()