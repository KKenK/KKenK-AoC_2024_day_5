from classes import page_line

def select_page_sort(page_ordering_rules_line_subdict, line):

    line_pages = [page.number for page in line.pages]

    current_page_index = 0

    while current_page_index < len(line_pages):

        current_page = line_pages[current_page_index]

        if current_page not in page_ordering_rules_line_subdict:
            current_page_index += 1
            continue
        
        current_page_values= page_ordering_rules_line_subdict[current_page]

        pages_to_insert_after_current_page = []
        indexs_of_rule_violating_pages = []
        
        for value_page_number in current_page_values:

            value_index = line_pages.index(value_page_number)
 
            if value_index > current_page_index:
                continue

            pages_to_insert_after_current_page.append(line_pages[value_index])
            
            indexs_of_rule_violating_pages.append(value_index)

        if not indexs_of_rule_violating_pages:
            current_page_index += 1
            continue

        line_pages = line_pages[:current_page_index + 1] + pages_to_insert_after_current_page + line_pages[current_page_index + 1:]

        indexs_of_rule_violating_pages = sorted(indexs_of_rule_violating_pages, reverse=True)

        for index in indexs_of_rule_violating_pages:
             line_pages.pop(index)           

        
        current_page_index -= len(pages_to_insert_after_current_page) + 1

    line = page_line.PageLine(line_pages)

    return line
