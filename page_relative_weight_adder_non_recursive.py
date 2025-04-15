class PageRelativeWeightAdder():
    def __init__(self, page_ordering_rules_dict):
        self._page_ordering_rules_dict = page_ordering_rules_dict    

    def add_relative_page_weights(self, line, line_index_sequence_dictionary):

        page_numbers = [page.number for page in line.pages]
     
        weight_increment = 0

        line_length = len(page_numbers)
        
        page_indexs = list(range(line_length))
        
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
