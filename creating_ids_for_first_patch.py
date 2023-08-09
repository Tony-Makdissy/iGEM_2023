import pandas as pd
import numpy as np

# define the dataframe coloumns
coloumns = ["patch","zip_name", "name", "contigs", "pdb", "iterations", "hotspot", "num_designs", "num_seqs", "initial_guess",
            "num_recycles", "use_multimer", "rm_aa", "mpnn_sampling_temp"]

# create the dataframe
df = pd.DataFrame(columns=coloumns)

rows = [
    {
        "zip_name": "HPV_capsid_around_the_pore_X137_6233t.result",
        "name": "HPV_capsid_around_the_pore_X137",
        "contigs": "B:C:D:E:F:20-40",
        "pdb": "/content/7kzf_reduced_around_X137.pdb",
        "hotspot": "B137,C137,D137,E137,F137",
        "num_designs": 2
    },
    {
        "zip_name": "HPV_capsid_around_the_pore_X137_auv2a.result",
        "name": "HPV_capsid_around_the_pore_X137",
        "contigs": "B:C:D:E:F:20-40",
        "pdb": "/content/7kzf_reduced_around_X137.pdb",
        "hotspot": "B137,C137,D137,E137,F137",
        "num_designs": 1
    },
    {
        "zip_name": "HPV_capsid_around_the_pore_X137_txkzl.result",
        "name": "HPV_capsid_around_the_pore_X137",
        "contigs": "B:C:D:E:F:20-40",
        "pdb": "/content/7kzf_reduced_around_X137.pdb",
        "hotspot": "B137,C137,D137,E137,F137",
        "num_designs": 2
    },
    {
        "zip_name": "HPV_capsid_inside_the_pore_X259.result",
        "name": "HPV_capsid_in_B126_to_B130_groove_of_126_to_135_structre ",
        "contigs": "B:C:D:E:F:20-40",
        "pdb": "/content/7kzf_reduced_around_X126_to_135.pdb",
        "hotspot": "B126,B127,B128,B129,B130",
        "num_designs": 8
    },
    {
        "zip_name": "HPV_capsid_in_B126_to_B130_groove_of_126_to_135_structre.result",
        "name": "HPV_capsid_in_B126_to_B130_groove_of_126_to_135_structre",
        "contigs": "B:C:D:E:F:20-40",
        "pdb": "/content/7kzf_reduced_around_X126_to_135.pdb",
        "hotspot": "B126,B127,B128,B129,B130",
        "num_designs": 1
    },
    {
        "zip_name": "HPV_capsid_in_B126_to_B130_groove_of_126_to_135_structre.result_2",
        "name": "HPV_capsid_in_B126_to_B130_groove_of_126_to_135_structre",
        "contigs": "B:C:D:E:F:20-40",
        "pdb": "/content/7kzf_reduced_around_X126_to_135.pdb",
        "hotspot": "B126,B127,B128,B129,B130",
        "num_designs": 2
    },
    {
        "zip_name": "HPV_capsid_in_B126_to_B130_groove_of_126_to_135_structre_0dcey.result",
        "name": "HPV_capsid_in_B126_to_B130_groove_of_126_to_135_structre",
        "contigs": "B:C:D:E:F:10-20",
        "pdb": "/content/7kzf_reduced_around_X126_to_135.pdb",
        "hotspot": "B126,B127,B128,B129,B130",
        "num_designs": 4
    },
    {
        "zip_name": "HPV_capsid_on_B39_42_65_447_479_groove.result",
        "name": "HPV_capsid_on_B39_42_65_447_479_groove",
        "contigs": "B:C:32-48",
        "pdb": "/content/7kzf_B39_42_65_447_449_r20.pdb",
        "hotspot": "B39,B42,B65,B447,B449",
        "num_designs": 8
    },
    {
        "zip_name": "HPV_capsid_on_B39_42_65_447_479_groove_from_complete_B_and_C.result",
        "name": "HPV_capsid_on_B39_42_65_447_479_groove_from_complete_B_and_C",
        "contigs": "B:C:32-48",
        "pdb": "7kzf",
        "hotspot": "B39,B42,B65,B447,B449",
        "num_designs": 1
    },
    {
        "zip_name": "HPV_capsid_on_B39_42_65_447_479_groove_from_complete_B_and_C.result_1",
        "name": "HPV_capsid_on_B39_42_65_447_479_groove_from_complete_B_and_C",
        "contigs": "B:C:70-80",
        "pdb": "7kzf",
        "hotspot": "B39,B42,B65,B447,B449",
        "num_designs": 4
    },
    {
        "zip_name": "HPV_capsid_on_B39_42_65_447_479_groove_from_complete_B_and_C.result_2",
        "name": "HPV_capsid_on_B39_42_65_447_479_groove_from_complete_B_and_C",
        "contigs": "B:C:70-80",
        "pdb": "7kzf",
        "hotspot": "B39,B42,B65,B447,B449",
        "num_designs": 4
    }
]

df = df._append(rows, ignore_index=True)
# fill the coloumn iterations with value 50
df["patch"] =  0
df["iterations"] = 50
df["num_seqs"] = 8
df["initial_guess"] = True
df["num_recycles"] = 3
df["use_multimer"] = False
df["rm_aa"] = "C"
df["mpnn_sampling_temp"] = 0.1

# sum the number of designs
print(df["num_designs"].sum())

# save a tsv file and name the index coloumn as id
df.to_csv("first_patch_runs_parameters.csv", index_label="run_id")
