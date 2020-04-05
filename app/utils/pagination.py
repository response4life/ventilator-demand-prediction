import math


def paginate(page, count, data, list_key):
    if page == None:
        page = 1
    else:
        page = int(page)

    if count == None:
        count = 25
    else:
        count = int(count)

    total = len(data[list_key])
    pages = math.ceil(total/count)

    if page > pages:
        page = pages

    page_range = [page * count - count, page * count]
    data[list_key] = data[list_key][page_range[0]:page_range[1]]
    data.update({'paging': {'total': total, 'page': page, 'pages': pages}})

    return data
