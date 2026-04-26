def get_subquery_depths(ranges: list[tuple[int, int]]) -> list[int]:
    depths = []
    for target_start, target_end in ranges:
        depth = 0
        for search_start, search_end in ranges:
            if target_start > search_start and target_end < search_end:
                depth += 1
        depths.append(depth)
    return depths
