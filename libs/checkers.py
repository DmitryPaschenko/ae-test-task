from abc import ABC, abstractmethod
from libs.html import HtmlElement


class Checker(ABC):
    """
    Base class for all required checkers
    """
    _orig_element = None
    _html_element = None

    def __init__(self, orig_element, html_element):
        if not isinstance(orig_element, HtmlElement) or not isinstance(html_element, HtmlElement):
            raise ValueError('"orig_element" and "html_element" parameters should be Instance of HtmlElement')
        self._orig_element = orig_element
        self._html_element = html_element

    @abstractmethod
    def check(self):
        raise NotImplemented()


class TextChecker(Checker):
    """
    Checker for check text two HTML elements
    """
    def check(self):
        return self._orig_element.text.strip() == self._html_element.text.strip()


class ClassChecker(Checker):
    """
    Checker for check css classes for two HTML elements
    """
    def check(self):
        return self._orig_element.get_element_attr('class') == self._html_element.get_element_attr('class')
