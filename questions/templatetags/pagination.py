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


@register.filter
def plural_answers(count):
    if count % 10 == 1 and count % 100 != 11:
        return 'ответ'
    elif count % 10 in [2, 3, 4] and count % 100 not in [12, 13, 14]:
        return 'ответа'
    else:
        return 'ответов'
