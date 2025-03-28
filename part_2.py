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
        self._line_page_ordering_sequence_dict = {}

    def add_relative_page_weights(self, line):
         
        pages_numbers = [x.number for x in line.pages]

        weight_increment = 0

        for current_page_index in range(len(line.pages)):
             
            line.pages[current_page_index].weight = weight_increment
     
            weight_increment += 1

            if line.pages[current_page_index].number not in self._page_ordering_rules_dict:
                continue
            
            line, weight_increment = self._recursively_traverse_page_ordering_rules_dict_reassigning_weights(line, pages_numbers, current_page_index, weight_increment)
        
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

    

    def _recursively_traverse_page_ordering_rules_dict_reassigning_weights(self, line, page_numbers, current_page_index, weight_increment):
        
        lower_page_weight_values = self._page_ordering_rules_dict[line.pages[current_page_index].number]
        
        lower_page_weight_values = set(lower_page_weight_values).intersection(set(page_numbers))
                
        lower_page_weight_value_indexs = [x for x in [page_numbers.index(y) for y in lower_page_weight_values] if x < current_page_index]
        

        #Get the lower_page_weight_indexs and remove the intersection with the proceeding
        if not lower_page_weight_value_indexs:
            return line, weight_increment
        
        for lower_page_weight_index in lower_page_weight_value_indexs:
            
            """
            # Check for multiple instances
            instances_of_lower_page_weight_indexs = [x for x,y in enumerate(page_numbers) if y == lower_page_weight]
            if len(instances_of_lower_page_weight_indexs) >= 2:
                print(instances_of_lower_page_weight_indexs)
            """

            line.pages[lower_page_weight_index].weight = weight_increment

            weight_increment += 1
            
            if line.pages[lower_page_weight_index].number not in self._page_ordering_rules_dict:
                continue

            self._recursively_traverse_page_ordering_rules_dict_reassigning_weights(line, page_numbers, lower_page_weight_index, weight_increment)
        
        return line, weight_increment

if __name__ == "__main__":

    input_parser = input_parser.InputParser(r"C:\Users\kylek\Documents\code\Advent_of_code\2024\Day_5\input.txt")

    page_ordering_rules_dict, pages_to_produce = input_parser.parsed_input

    line_page_order_analyser = LineCorrectlyOrderedChecker(page_ordering_rules_dict)
    page_relative_weight_adder = PageRelativeWeightAdder(page_ordering_rules_dict)
    
    middle_page_number_total = 0
    
    for line in pages_to_produce:
        
        line = PageLine(line)
        #line.print_line()  
        if line_page_order_analyser.is_line_correctly_ordered(line):
            continue
        
        line_rules_dict = page_relative_weight_adder._create_line_based_rule_dictionary()

        #correctly_sorted_pages_numbers = [page.number for page in sorted(line.pages, key= lambda x : x.weight)]
        #print(correctly_sorted_pages_numbers)
        #middle_page_number_total += MiddlePageGetter.get_middle_line(correctly_sorted_pages_numbers)
    
    print(middle_page_number_total)
    
