from rest_framework.pagination import PageNumberPagination


class PageLimitPagination(PageNumberPagination):
    """
    Пагинатор с определением атрибута
    для вывода запрошенного количества страниц.
    """
    page_size = 6
    page_size_query_param = 'limit'
