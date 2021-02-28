import math
from typing import List, Optional


class PagePagination:
    page = 1

    def __init__(self, items, page, page_size, total, schema=None):
        self.page = page
        self.items: list = items
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.total = total.pop() if isinstance(total, list) else total
        self.has_next = previous_items + len(items) < self.total
        if self.has_next:
            self.next_page = page + 1
        self.pages = int(math.ceil(self.total / float(page_size)))

        if schema:
            self.schema = schema
            self._cast_to_schema()

    def _cast_to_schema(self):
        self.items.remove(None)  # remove from response `null` element
        return [self.schema.from_orm(item) for item in self.items]

    @classmethod
    def get_query(cls, query):
        _page = cls.page
        return query.limit(_page).offset((_page - 1) * _page)

    def meta_response(self, items: Optional[List] = None):
        return {
            'items': items or self.items,
            'meta_info': {
                'page': self.page,
                'pages': self.pages,
                'total': self.total,
                'has_next': self.has_next,
                'has_previous': self.has_previous,
            }
        }
