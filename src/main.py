from textnode import *
from htmlnode import *

def main():
    test_text = TextNode("I love waffles", TextType.BOLD, url = "https://www.boot.dev")
    print(test_text)

def text_node_to_html_node(html_node):
    if html_node.text_type == TextType.NORMAL:
        return LeafNode(None, html_node.text, None)
    
    elif html_node.text_type == TextType.BOLD:
        return LeafNode("b", html_node.text, None)
    
    elif html_node.text_type == TextType.ITALIC:
        return LeafNode("i", html_node.text, None)
    
    elif html_node.text_type == TextType.CODE:
        return LeafNode("code", html_node.text, None)
    
    elif html_node.text_type == TextType.LINK:
        return LeafNode("a", html_node.text, {"href" : html_node.url})
    
    elif html_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src" : html_node.url, "alt" : html_node.text})
    
    else:
        raise ValueError(f"The provided HTML_Node's type doesn't match the existing types: {html_node.text_type}")


if __name__ == "__main__":
    main()