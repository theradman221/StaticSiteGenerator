

class HTMLNode():
    def __init__(self, tag= None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        pass

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props == None:
            return ""
        else:
            return_string = ""
            for key in self.props:
                return_string += f" {key}=\"{self.props[key]}\""
            return return_string
        
    def __repr__(self):
        return f"HTMLNode Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props: {self.props}"
    
class LeafNode(HTMLNode):
    # Removed Children from LeafNode since these nodes should have no children
    def __init__(self, tag=None, value = None, props=None):
        if value == None:
            raise ValueError("LeafNodes must have a value!")
        super().__init__(tag = tag, value = value, props = props) 

    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value")
        elif self.tag == None:
            return self.value
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag = tag, children = children, props =  props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Parent Nodes must have a tag")
        elif self.children == None or len(self.children) == 0:
            raise ValueError("Parent nodes must have a child Node")
        string = f"<{self.tag}>{self.props_to_html()}"
        for value in self.children:
            string += value.to_html()
        string += f"</{self.tag}>"
        return string
        
