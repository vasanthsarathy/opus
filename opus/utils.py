# Given a list of dictionaries, and a key, return the entry in the list that matches
def find_dict_in_list(lst, key, target):
    for item in lst:
        if not key in item:
            #print("Key not in Dict")
            return None
        if item[key] == target:
            return item
    #print("Nothing found")
    return None

def find_all_dicts_in_list(lst, key, target):
    output = []
    for item in lst:
        if not key in item:
            return output
        if item[key] == target:
            output.append(item)
    #print("Nothing found")
    return output
