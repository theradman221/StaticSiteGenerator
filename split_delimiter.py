import re
from textnode import TextNode

# Splits a old_nodes list / string and returns that as a list with any delimiters split out
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    return_list = []
    for node in old_nodes:
        # Make sure there is an opening and closing instance of the delimiter in the nodes text, or raise an exception if there isn't
        text = node.text
        if text.count(delimiter) % 2 != 0 and text.count(delimiter) > 0:
            raise ValueError("There is no closing delimiter in this node")
        splits = text.split(delimiter)
        index = 0
        for split in splits:
            if index % 2 != 0:
                # evens will be delimiter types, since you should always get an odd amount of splits from a successful split, and this is an index
                return_list.append(TextNode(split, text_type))
            else:
                return_list.append(TextNode(split, node.text_type))
            index += 1
    return return_list

def split_nodes_image(old_nodes):
    return

def split_nodes_link(old_nodes):
    return

def extract_markdown_images(text):
    extracted_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_text

def extract_markdown_links(text):
    extracted_text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_text
            
