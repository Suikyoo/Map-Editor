import os 
from scripts import core_functs, map_functs

path = "judea/Desktop/pain.exe"
path = os.path.splitext(os.path.split(path)[1])[0]
d = {"hahahah" : 
        {"ohohohoh" : 
            {"ehehehe" : 5}
        }, 
    "yeahhh" :
        {"nawww" : 
            {"ohhoohho" :
                10
            }
        },
    }

d = core_functs.read_json("map/level_1.json")["tile"]
dict_level = 2


index = 0
lst = [list(i.keys()) for i in core_functs.data_lift(d, dict_level)]

print(core_functs.granify_list(lst, 2))
print(len(core_functs.mince_list(lst, 2)))
