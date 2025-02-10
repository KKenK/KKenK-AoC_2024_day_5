class InputParser():

    def __init__(self, input_path):

        input = []

        with open(input_path) as f:
            input = f.read()

        self.parsed_input = self._parse_file(input)

    def _parse_file(self, input):

        page_ordering_rules, pages_to_produce = input.split("\n\n")
    
        page_ordering_rules = [[int(y) for y in x.split("|")] for x in page_ordering_rules.split("\n")]

        page_ordering_rules_dict = {x[0] : [] for x in page_ordering_rules}

        for ordering_rule in page_ordering_rules:
            page_ordering_rules_dict[ordering_rule[0]].append(ordering_rule[1])
        
        pages_to_produce = [[int(y) for y in x.split(",")] for x in pages_to_produce.split("\n")]

        return page_ordering_rules, pages_to_produce

if __name__ == "__main__":

    input_parser = InputParser(r"C:\Users\kylek\Documents\code\Advent_of_code\2024\Day_5\test.txt")

    print(input_parser.parsed_input)