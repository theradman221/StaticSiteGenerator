print("hello world")

from textnode import *

def main():
    test_text = TextNode("I love waffles", TextType.bold, url = "https://www.boot.dev")
    print(test_text)


main()