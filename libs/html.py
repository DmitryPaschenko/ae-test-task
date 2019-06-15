class HtmlElement(object):
    '''
    HTML element based on bs4 HTML element object
    '''
    __bs_element = None
    attrs = []
    text = ''

    def __init__(self, bs_element):
        self.__bs_element = bs_element
        self.attrs = bs_element.attrs
        self.text = bs_element.text.strip()
        self.tag_name = bs_element.name

    def get_element_attr(self, attr):
        return self.attrs.get(attr, None)
