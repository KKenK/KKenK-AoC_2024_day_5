def get_middle_page(line):
    
    if len(line) % 2 != 0:
        return line[len(line) // 2]

    return line[(len(line) // 2) - 1]