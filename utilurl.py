def enumerate_dict_and_list(it):
    return it.items() if isinstance(it, dict) else enumerate(it)

def level_to_one(paramsin):
    paramsout = {}
    for index, value in enumerate_dict_and_list(paramsin):
        level_to_one_aux(value, index, paramsout)
    return paramsout

def level_to_one_aux(paramsin, key, paramsout):
    if not isinstance(paramsin, (list, dict, tuple)):
        paramsout[key] = paramsin
    else:
        for index, value in enumerate_dict_and_list(paramsin):
            level_to_one_aux(value, str(key) + '[' + str(index) + ']', paramsout)

