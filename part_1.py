import input_parser
from collections import namedtuple

Page = namedtuple("Page", ["number", "preceding_pages", "proceeding_pages"])

class PageLine():
    def __init__(self, line):
        self.pages = self._make_line(line)

    def _make(self, line):

        pages = []

        for i in range(len(line)):

            proceeding_pages = line[i:]

            proceeding_pages.pop(0)

            pages.append(Page(number = line[i], preceding_pages= set(line[:i]), proceeding_pages = set(proceeding_pages)))

        return pages

    def print_line(self):
        
        for page in self.pages:
            print(page.number, sep=",", end=" ")
        
        print(" ")

class LineCorrectlyOrderedChecker():

    def __init__(self, page_ordering_rules_dict):
        self._page_ordering_rules_dict = page_ordering_rules_dict

    def check(self, line):

        for page in line.pages:

            if page.number not in self._page_ordering_rules_dict:
                continue

            if page.preceding_pages.intersection(self._page_ordering_rules_dict[page.number]):
                return False

            if not page.proceeding_pages.intersection(self._page_ordering_rules_dict[page.number]):
                
                if page == line.pages[-1]:
                    continue

                return False    
        
        return True

class MiddlePageGetter():
    @staticmethod
    def get_middle_line(line):
        
        if len(line) % 2 != 0:
            return line[len(line) // 2]
        
        return line[(len(line) // 2) - 1]

if __name__ == "__main__":

    input_parser = input_parser.InputParser(r"C:\Users\kylek\Documents\code\Advent_of_code\2024\Day_5\input.txt")

    page_ordering_rules_dict, pages_to_produce = input_parser.parsed_input

    line_page_order_analyser = LineCorrectlyOrderedChecker(page_ordering_rules_dict)

    middle_page_number_total = 0
    
    for line in pages_to_produce:
        if not line_page_order_analyser.is_line_correctly_ordered(PageLine(line)):
            continue

        middle_page_number_total += MiddlePageGetter.get_middle_line(line)
    
    print(middle_page_number_total)
    
