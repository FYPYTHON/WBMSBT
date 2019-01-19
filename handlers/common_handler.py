# coding=utf-8

PAGESIZE = 5
FIRST_PAGE = 1


def get_pages(total_page):
    pages = total_page // PAGESIZE + 1
    return pages