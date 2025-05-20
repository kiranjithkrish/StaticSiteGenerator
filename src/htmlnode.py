from functools import reduce

class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        attributed_string = reduce(lambda acc, key_val: acc + f' {key_val[0]}="{key_val[1]}"', self.props.items(), "")
        return attributed_string

    def __repr__(self):
        children_str = str(self.children) if self.children is not None else "None"
        props_str = str(self.props) if self.props is not None else "None"
        return f'HTMLNode(tag={self.tag}, value={self.value}, children={children_str}, props={props_str})'

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError
        if self.tag is None:
            return self.value
        props_str = super().props_to_html()
        return f'<{self.tag}{props_str}>{self.value}</{self.tag}>'
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, None, None)
        self.children = children
        self.props = props
        
    def to_html(self):
        if len(self.tag) == 0:
            raise ValueError
        if len(self.children) == 0:
            raise ValueError('Empty children')
        
        props_str = self.props_to_html()
        res = f'<{self.tag}{props_str}>'
        for child in self.children:
            res += child.to_html()
        res += f'</{self.tag}>'
        return res
        
        
        

