
def puncture_higher(input_arr, no_punctured_scs):
    for i in range(len(input_arr)-no_punctured_scs, len(input_arr)):
        input_arr[i] = 0
    return input_arr


def puncture_lower(input_arr, no_punctured_scs):
    for i in range(0, no_punctured_scs):
        input_arr[i] = 0
    return input_arr
