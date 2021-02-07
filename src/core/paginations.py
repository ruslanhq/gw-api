import math


class PagePagination:
    page = 1

    def __init__(self, items, page, page_size, total):
        self.page = page
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.has_next = previous_items + len(items) < total
        if self.has_next:
            self.next_page = page + 1
        self.total = total
        self.pages = int(math.ceil(total / float(page_size)))

    @classmethod
    def get_query(cls, query):
        _page = cls.page
        return query.limit(_page).offset((_page - 1) * _page).all()
