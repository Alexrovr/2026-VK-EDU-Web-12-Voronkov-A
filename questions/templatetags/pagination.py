from django import template

register = template.Library()


@register.filter
def smart_pagination(page, neighbors=2):
    paginator = page.paginator
    total_pages = paginator.num_pages
    current_num = page.number

    if total_pages <= 7:
        return list(paginator.page_range)

    pages = []

    pages.append(1)

    start = max(2, current_num - neighbors)
    end = min(total_pages - 1, current_num + neighbors)

    if start > 2:
        pages.append('...')

    pages.extend(range(start, end + 1))

    if end < total_pages - 1:
        pages.append('...')

    pages.append(total_pages)

    return pages
