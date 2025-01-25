import unittest

from textnode import TextNode, TextType
from split_delimiter import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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

    # Test the split_delimiter function
    def test_delimiter(self):
        # Test mismatched delimiter error
        with self.assertRaises(ValueError):
            node = TextNode("This will *be mismatched!", TextType.NORMAL)
            failure = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_lists = [] # These should both be inserted to in the same order or you will be testing different test results
        result_lists = []

        test_node_none = TextNode("Oh what a lovely day for no splits", TextType.NORMAL)
        expected_lists.append([TextNode("Oh what a lovely day for no splits", TextType.NORMAL)])
        
        test_node_bold = TextNode("Single **bold** word", TextType.NORMAL)
        expected_lists.append([TextNode("Single ", TextType.NORMAL), TextNode("bold", TextType.BOLD), TextNode(" word", TextType.NORMAL)])
        
        test_node_bold_long = TextNode("Multiple **bolded** words in a sentance **is really fun**!", TextType.NORMAL)
        expected_lists.append([TextNode("Multiple ", TextType.NORMAL), TextNode("bolded", TextType.BOLD), TextNode(" words in a sentance ", TextType.NORMAL), TextNode("is really fun", TextType.BOLD), TextNode("!", TextType.NORMAL)])
        
        test_node_italic = TextNode("this *should* be italics!", TextType.NORMAL)
        expected_lists.append([TextNode("this ", TextType.NORMAL), TextNode("should", TextType.ITALIC), TextNode(" be italics!", TextType.NORMAL)])

        test_node_single_bold = TextNode("**BOLD**", TextType.NORMAL)
        expected_lists.append([TextNode("", TextType.NORMAL), TextNode("BOLD", TextType.BOLD), TextNode("", TextType.NORMAL)])

        test_looping_types = TextNode("Going 4to4 .use. *multiple* **delimiters** in a 'loop' to make sure it @works@ properly", TextType.NORMAL)
        expected_lists.append([
            TextNode("Going ", TextType.NORMAL), TextNode("to", TextType.IMAGE), TextNode(" ", TextType.NORMAL), TextNode("use", TextType.CODE),
            TextNode(" ", TextType.NORMAL), TextNode("multiple", TextType.ITALIC), TextNode(" ", TextType.NORMAL), TextNode("delimiters", TextType.BOLD),
            TextNode(" in a ", TextType.NORMAL), TextNode("loop", TextType.CODE), TextNode(" to make sure it ", TextType.NORMAL), TextNode("works", TextType.LINK),
            TextNode(" properly", TextType.NORMAL)
        ])

        # Process all test TextNodes into lists and compare the lists to the correct lists
        none_list = split_nodes_delimiter([test_node_none], "**", TextType.BOLD) # There shouldn't be any splits in this list
        result_lists.append(none_list)
        bold_list = split_nodes_delimiter([test_node_bold], "**", TextType.BOLD) # This should result in a list like this, but with normal, bold, normal types [single, bold, word]
        result_lists.append(bold_list)
        bold_list_long = split_nodes_delimiter([test_node_bold_long], "**", TextType.BOLD)
        result_lists.append(bold_list_long)
        italic_list = split_nodes_delimiter([test_node_italic], "*", TextType.ITALIC)
        result_lists.append(italic_list)
        bold_single_list = split_nodes_delimiter([test_node_single_bold], "**", TextType.BOLD)
        result_lists.append(bold_single_list)

        # Test the looping to get multiple types of delimiters
        looping_list = split_nodes_delimiter([test_looping_types], "**", TextType.BOLD)
        looping_list = split_nodes_delimiter(looping_list, "4", TextType.IMAGE)
        looping_list = split_nodes_delimiter(looping_list, "'", TextType.CODE)
        looping_list = split_nodes_delimiter(looping_list, "@", TextType.LINK)
        looping_list = split_nodes_delimiter(looping_list, ".", TextType.CODE)
        looping_list = split_nodes_delimiter(looping_list, "*", TextType.ITALIC)
        result_lists.append(looping_list)
        index = 0
        while index < len(expected_lists) and index < len(result_lists):
            inner_index = 0
            while inner_index < len(expected_lists[index]) and inner_index < len(result_lists[index]):
                self.assertEqual(expected_lists[index][inner_index], result_lists[index][inner_index])
                inner_index += 1
            index += 1

    def test_markdown_extractors(self):
        # Pulled these examples from boot.dev
        text_image = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        test_link = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        images = extract_markdown_images(text_image)
        link = extract_markdown_links(test_link)

        self.assertEqual(extract_markdown_links(text_image), []) # Links shouldn't match images
        self.assertEqual(extract_markdown_images(test_link), []) # Images shouldn't match links
        self.assertEqual(images[0][0], "rick roll")
        self.assertEqual(images[1][0], "obi wan")
        self.assertEqual(link[0][0], "to boot dev")
        self.assertEqual(link[1][0], "to youtube")

        simple_link = "This is a link [who knows where it goes?](notme!) it really is weird!"
        self.assertEqual(extract_markdown_links(simple_link), [("who knows where it goes?", "notme!")])




if __name__ == "__main__":
    unittest.main()