def get_unique_list(seq):
    seen = []
    return [x for x in seq if x not in seen and not seen.append(x)]