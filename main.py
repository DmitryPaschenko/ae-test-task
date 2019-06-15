from abc import ABC, abstractmethod
from bs4 import BeautifulSoup


class HtmlElement(object):
    '''
    HTML element based on bs4 HTML element object
    '''
    __bs_element = None
    attrs=[]
    text=''

    def __init__(self, bs_element):
        self.__bs_element = bs_element
        self.attrs = bs_element.attrs
        self.text = bs_element.text.strip()
        self.tag_name = bs_element.name

    def get_element_attr(self, attr):
        return self.attrs.get(attr, None)


class Checker(ABC):
    '''
    Base class for all required checkers
    '''
    _orig_element = None
    _html_element = None

    def __init__(self, orig_element, html_element):
        self._orig_element = orig_element
        self._html_element = html_element

    @abstractmethod
    def check(self):
        raise NotImplemented()


class TextChecker(Checker):
    '''
    Checker for check text two HTML elements
    '''
    def check(self):
        return self._orig_element.text.strip() == self._html_element.text.strip()


class ClassChecker(Checker):
    '''
    Checker for check css classes for two HTML elements
    '''
    def check(self):
        return self._orig_element.get_element_attr('class') == self._html_element.get_element_attr('class')


def same(orig_element, html_element, checkers):
    '''
    Compare two html elements according passed checkers
    :param orig_element:
    :param html_element:
    :param checkers:
    :return:
    '''
    return all([check_class(orig_element, html_element).check() for check_class in checkers])


def has_same_element(file_path, orig_element):
    '''
    Check if "different" file has origin elements
    :param file_path:
    :param orig_element:
    :return:
    '''

    checkers = [
        TextChecker,
        ClassChecker,  # if you want more checks just create checker and add it to this list
    ]

    tag_name = orig_element.tag_name

    with open(file_path, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.find_all(tag_name)
        for element in elements:
            html_element = HtmlElement(bs_element=element)
            if same(orig_element, html_element, checkers):
                return True

    return False


def get_element_info(file_path, css_selector):
    with open(file_path, 'r') as f:
        content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        elements = soup.select(css_selector)
        if len(elements) == 0:
            raise Exception('Element Not Found In Original Document')
        else:
            element = elements[0]

        html_element = HtmlElement(bs_element=element)

        return html_element


if __name__ == '__main__':
    css_selector = 'a[id=make-everything-ok-button]'
    orig_file_path = 'res/sample-0-origin.html'
    diff_file_path = 'res/sample-1-evil-gemini.html'

    orig_element_info = get_element_info(orig_file_path, css_selector)
    print('File "{}" HAS {}same element'.format(
        diff_file_path,
        '' if has_same_element(diff_file_path, orig_element_info) else 'NOT '
    ))

