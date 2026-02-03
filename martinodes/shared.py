CATEGORY = "martinodes"

def list_head_tail(list, take_count, start_end):

    total = list.shape[0]
    take_count = min(take_count, total)

    if start_end == "start":
        new_list = list[:take_count]
    else:
        new_list = list[-take_count:]

    return new_list
    