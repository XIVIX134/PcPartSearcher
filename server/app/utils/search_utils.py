def format_search_results(results):
    total_items = sum(len(items) for items in results.values())
    response_data = {
        **results,
        'totalItems': total_items,
        'totalPages': (total_items // 24) + (1 if total_items % 24 > 0 else 0),
        'itemsPerPage': 24,
        'status': 'success'
    }
    return response_data
