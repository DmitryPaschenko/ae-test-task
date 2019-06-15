import sys
from bs4 import BeautifulSoup

from libs.html import HtmlElement
from libs.checkers import ClassChecker, TextChecker


def same(orig_element, html_element, checkers):
    """
    Compare two html elements according passed checkers
    :param orig_element:
    :param html_element:
    :param checkers:
    :return:
    """

    return all([check_class(orig_element, html_element).check() for check_class in checkers])


def has_same_element(file_path, orig_element):
    """
    Check if "different" file has origin elements
    :param file_path:
    :param orig_element:
    :return:
    """

    checkers = [
        TextChecker,
        ClassChecker,  # if you want to add more checks just create checker and add it to this list
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
    """
    Get info about target element

    :param file_path: Path to original HTML file
    :param css_selector: Css Selector of target HTML element
    :return: HtmlElement
    """

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
    if len(sys.argv) >= 3:
        orig_file_path = sys.argv[1]
        diff_file_path = sys.argv[2]
    else:
        orig_file_path = 'res/sample-0-origin.html'
        diff_file_path = 'res/sample-1-evil-gemini.html'

    css_selector = 'a[id=make-everything-ok-button]'
    orig_element_info = get_element_info(orig_file_path, css_selector)
    print('File "{}" HAS {}same element'.format(
        diff_file_path,
        '' if has_same_element(diff_file_path, orig_element_info) else 'NOT '
    ))
