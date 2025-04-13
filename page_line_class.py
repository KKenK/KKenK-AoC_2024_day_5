import page

class PageLine():
    def __init__(self, line):
        self.pages = self._make(line)

    def _make(self, line):

        pages = []

        for i in range(len(line)):

            proceeding_pages = line[i:]

            proceeding_pages.pop(0)

            pages.append(page.Page(number = line[i], preceding_pages= set(line[:i]), proceeding_pages = set(proceeding_pages)))

        return pages

