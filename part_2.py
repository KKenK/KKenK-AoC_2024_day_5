import input_parser
import page_line_class
import select_style_page_sort
from collections import namedtuple

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

    def add_relative_page_weights(self, line, line_index_sequence_dictionary):

        page_numbers = [page.number for page in line.pages]
     
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

class LinePageOrderingRulesSubdictionary():

    def __init__(self, page_ordering_rules_dict):

        self.page_ordering_rules_dict = page_ordering_rules_dict

    def create_line_rules_sub_dictionary(self, page_ordering_rules_dict, page_numbers):

        line_rules_sub_dict = {}

        for page in page_numbers:

            if page not in page_ordering_rules_dict:
                continue    
            
            line_rules_sub_dict[page] = [x for x in page_numbers if x in page_ordering_rules_dict[page]]
        
        return line_rules_sub_dict


def nested_page_rules_dictionary(self, keys):

    nested_rules_dict = {}

    for item in keys:

        item_values = []  
        
        for value in page_ordering_rules_line_subdict[item]:

            if value not in self.page_ordering_rules_line_subdict:
                item_values.append(value)
                continue

            item_values.append(self._nested_page_rules_dictionary([value]))

        nested_rules_dict[item] = item_values

    return nested_rules_dict

def create_line_rules_index_sequence_dictionary(page_ordering_rules_line_subdict, page_numbers):
    
    line_index_sequence_dictionary = {}

    for page in page_numbers:
        
        if page not in page_ordering_rules_line_subdict:
            continue

        line_index_sequence_dictionary[page] = sorted([page_numbers.index(x) for x in page_ordering_rules_line_subdict[page]])
        
    return line_index_sequence_dictionary
    
if __name__ == "__main__":

    input_parser = input_parser.InputParser(r"C:\Users\kylek\Documents\code\Advent_of_code\2024\Day_5\input.txt")

    page_ordering_rules_dict, pages_to_produce = input_parser.parsed_input

    line_page_order_analyser = LineCorrectlyOrderedChecker(page_ordering_rules_dict)
    page_relative_weight_adder = PageRelativeWeightAdder(page_ordering_rules_dict)
    
    line_page_ordering_rules_subdictionary = LinePageOrderingRulesSubdictionary(page_ordering_rules_dict)
    
    middle_page_number_total = 0
    
    for line in pages_to_produce:
        
        line = page_line_class.PageLine(line)

        if line_page_order_analyser.is_line_correctly_ordered(line):
            continue
        
        page_numbers = [page.number for page in line.pages]
        
        page_ordering_rules_line_subdict = line_page_ordering_rules_subdictionary.create_line_rules_sub_dictionary(page_ordering_rules_dict, page_numbers)
        line_index_sequence_dictionary = create_line_rules_index_sequence_dictionary(page_ordering_rules_line_subdict, page_numbers)

        #line = page_relative_weight_adder.add_relative_page_weights(line, line_index_sequence_dictionary)

        #correctly_sorted_pages_numbers = [page.number for page in sorted(line.pages, key= lambda x : x.weight)]

        correct_select_sorted_page_numbers = select_style_page_sort.select_page_sort(page_ordering_rules_line_subdict, line)
      
        while not line_page_order_analyser.is_line_correctly_ordered(correct_select_sorted_page_numbers):

            correct_select_sorted_page_numbers = select_style_page_sort.select_page_sort(page_ordering_rules_line_subdict, correct_select_sorted_page_numbers)
        
        correct_select_sorted_page_numbers = [page.number for page in correct_select_sorted_page_numbers.pages]

        #if correctly_sorted_pages_numbers != correct_select_sorted_page_numbers:
            #print(f"Weighted sort: {correctly_sorted_pages_numbers}")
            #print(f"Select sort: {correct_select_sorted_page_numbers}")
            #quit()

        middle_page_number_total += MiddlePageGetter.get_middle_line(correct_select_sorted_page_numbers)
    
    print(middle_page_number_total)
    