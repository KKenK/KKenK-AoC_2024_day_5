import input_parser
from collections import namedtuple

class Page():
    def __init__(self, number, preceding_pages, proceeding_pages):
        self.number =  number
        self.preceding_pages = preceding_pages
        self.proceeding_pages = proceeding_pages

class PageLine():
    def __init__(self, line):
        self.pages = self._make(line)

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

    def is_line_correctly_ordered(self, line):

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

class PageRelativeWeightAdder():
    def __init__(self, page_ordering_rules_dict):
        self._page_ordering_rules_dict = page_ordering_rules_dict    
        self.page_ordering_rules_line_subdict = {}
    def add_relative_page_weights(self, line):

        page_numbers = [page.number for page in line.pages]
     
        self.page_ordering_rules_line_subdict = self._create_line_rules_sub_dictionary(page_numbers)
        line_index_sequence_dictionary = self._create_line_rules_index_sequence_dictionary(page_numbers, self.page_ordering_rules_line_subdict)
        print(self.page_ordering_rules_line_subdict)
        nested_rules_dict = self._nested_page_rules_dictionary(self.page_ordering_rules_line_subdict.keys())
        print(nested_rules_dict)
        weight_increment = 0

        line_length = len(page_numbers)
        
        page_indexs = list(range(line_length))

        #print(page_indexs)
        
        index = 0
        while index < line_length: 
            
            line.pages[page_indexs[index]].weight = weight_increment

            weight_increment += 1

            if page_numbers[page_indexs[index]] not in line_index_sequence_dictionary:
                index += 1
                continue
           
            violating_page_indexs = [x for x in line_index_sequence_dictionary[page_numbers[page_indexs[index]]] if x < index]
            
            if not violating_page_indexs:
                index += 1
                continue
            
            page_indexs = page_indexs[:index + 1] + violating_page_indexs + page_indexs[index + 1:]
            
            line_length += len(violating_page_indexs)

            index += 1

        return line
    
    def create_line_based_rule_dictionary(self, page_numbers):
        
        line_rules_dict = {}

        if len(page_numbers) == 1:
            return page_numbers
        
        for page_number in page_numbers:

            if page_number not in self._page_ordering_rules_dict:
                continue

            subsequent_pages = self._page_ordering_rules_dict[page_number].intersection(page_numbers)

            if subsequent_pages == 0:
                continue

            for subsequent_page in subsequent_pages:
                line_rules_dict[page_number] = self._create_line_based_rule_dictionary(subsequent_page, page_numbers)

        return line_rules_dict
    
    def _create_line_rules_sub_dictionary(self, page_numbers):

        line_rules_sub_dict = {}

        for page in page_numbers:

            if page not in self._page_ordering_rules_dict:
                continue    
            
            line_rules_sub_dict[page] = [x for x in page_numbers if x in self._page_ordering_rules_dict[page]]
        
        return line_rules_sub_dict

    def _create_line_rules_index_sequence_dictionary(self, page_numbers, page_ordering_rules_line_subdict):
        
        line_index_sequence_dictionary = {}

        for page in page_numbers:
            
            if page not in page_ordering_rules_line_subdict:
                continue

            line_index_sequence_dictionary[page] = sorted([page_numbers.index(x) for x in page_ordering_rules_line_subdict[page]])
            
        return line_index_sequence_dictionary
    
    def _nested_page_rules_dictionary(self, keys):

        nested_rules_dict = {}

        for item in keys:

            item_values = []  
            
            for value in self.page_ordering_rules_line_subdict[item]:

                if value not in self.page_ordering_rules_line_subdict:
                    item_values.append(value)
                    continue

                item_values.append(self._nested_page_rules_dictionary([value]))

            nested_rules_dict[item] = item_values

        return nested_rules_dict
              
if __name__ == "__main__":

    input_parser = input_parser.InputParser(r"C:\Users\kylek\Documents\code\Advent_of_code\2024\Day_5\test_incorrect_line.txt")

    page_ordering_rules_dict, pages_to_produce = input_parser.parsed_input

    line_page_order_analyser = LineCorrectlyOrderedChecker(page_ordering_rules_dict)
    page_relative_weight_adder = PageRelativeWeightAdder(page_ordering_rules_dict)
    
    middle_page_number_total = 0
    
    for line in pages_to_produce:
        
        line = PageLine(line)
        #line.print_line()  
        if line_page_order_analyser.is_line_correctly_ordered(line):
            continue
        #print([page.number for page in line.pages])
        page_numbers = [page.number for page in line.pages]
        line = page_relative_weight_adder.add_relative_page_weights(line)

        correctly_sorted_pages_numbers = [page.number for page in sorted(line.pages, key= lambda x : x.weight)]
    
        #print(correctly_sorted_pages_numbers)
        middle_page_number_total += MiddlePageGetter.get_middle_line(correctly_sorted_pages_numbers)
    
    print(middle_page_number_total)
    
