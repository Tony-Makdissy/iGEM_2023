import BioPython_structure_handling as bsh
import json
import pandas as pd

# TODO: define the contigs, pdb

# read the file named "para_list.json" and convert it to a dictionary
with open("para_list.json", "r") as f:
    para_list = json.load(f)

# print the dictionary key
paramters_01_2 = pd.DataFrame(columns=para_list[0].keys())
for i in para_list:
    paramters_01_2 = paramters_01_2._append(i, ignore_index=True)

# hotspot
