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
