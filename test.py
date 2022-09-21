import core_functs

#used to drill a dictionary and input values
def data_pierce(dict, key_list, tip={}):
    if len(key_list) > 0:
        if len(key_list) == 1:
            ret_val = tip
        else: 
            ret_val = {}

        dict[key_list[0]] = dict.get(key_list[0], ret_val)
        data_pierce(dict[key_list[0]], key_list[1:], tip=tip)


#tries to retrieve data specified in the dictionary path
#returns None if dictionary path doesn't exist
#kinda sounds like a scout right?
def data_scout(dict, key_list):
    temp_dict = dict.copy()
    for i in key_list:
        if type(temp_dict) == type(dict):
            temp_dict = temp_dict.get(i)
            if temp_dict == None:
                return None
        else: return None

    return temp_dict

def replicate_dict(dictionary):
    def recursion(dict):
        if type(dict) == type({}):
            for i in dict:
                dict[i] = dict[i].copy()
                recursion(dict[i])

    dictionary = dictionary.copy() 
    recursion(dictionary)
    return dictionary

def prune_dict(item, blank_val={}):
    if isinstance(item, dict):
        if len(item):
            for k in item.copy(): 
                item[k] = prune_dict(item[k], blank_val=blank_val)
                if item[k] == blank_val: 
                    item.pop(k)

        else: 
            return blank_val

    elif item == blank_val:
        return blank_val


def prune_dict(item, blank_val={}):
    if isinstance(item, dict):
        for k in item.copy():
            v = prune_dict(item[k], blank_val=blank_val)
            if v == blank_val:
                item.pop(k)
            if not len(item):
                item = blank_val

    elif item == blank_val:
        return blank_val

    return item


d = {
        0 : {
            50 : {"hello1" : 1, "hello2" : None, "hello3" : "HELLO"},
            20 : {"hello4" : None, "hello5" : "HELLO", "hello6" : "HELLO"},
            30 : {"hello7" : None, "hello8" : None, "hello9" : None}
            }
    }

