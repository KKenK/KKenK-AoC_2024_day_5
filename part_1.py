from classes import input_parser
from classes import page_line
from classes import line_is_correctly_ordered_checker
from modules.get_middle_page import get_middle_page
from collections import namedtuple

if __name__ == "__main__":

    input_parser = input_parser.InputParser(r"C:\Users\kylek\Documents\code\Advent_of_code\2024\Day_5\input.txt")

    page_ordering_rules_dict, pages_to_produce = input_parser.parsed_input

    line_page_order_analyser = line_is_correctly_ordered_checker.LineCorrectlyOrderedChecker(page_ordering_rules_dict)

    middle_page_number_total = 0
    
    for line in pages_to_produce:
        if not line_page_order_analyser.is_line_correctly_ordered(page_line.PageLine(line)):
            continue

        middle_page_number_total += get_middle_page(line)
    
    print(middle_page_number_total)
    
