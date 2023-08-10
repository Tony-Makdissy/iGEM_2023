# https://www.machinelearningplus.com/python/parallel-processing-python/?expand_article=1

import multiprocessing as mp
import time
import os
import pandas as pd

# read "sequences_summary.csv" and "firs_patch_runs_parameters.csv" into dataframes
sequences_summary = pd.read_csv("sequences_summary.csv")
runs_parameters = pd.read_csv("first_patch_runs_parameters.csv")


# pick only the valid sequences, i.e. the ones that are not disregarded
valid_seq_ids = sequences_summary[sequences_summary["disregard"] == False]
# add a coloumn called "avg_score" to the dataframe
valid_seq_ids["avg_score"] = 0

# go over the sequence_global_id
for i in valid_seq_ids["sequence_global_id"]:
    # go the file containing the docking scores
    seq_doc_dir = f"HDOCK_docking_scores_copy/sequence{int(i):04d}"
    # read the ten files called "models_1.pdb" to "models_10.pdb"
    # then get the number in the fourth row which looks like ...
    # "REMARK Score:  X" where X is the score

    avg_score = 0

    for j in range(1,11):
        # read the file
        with open(f"{seq_doc_dir}/model_{j}.pdb", "r") as f:
            # read the fourth line
            line = f.readlines()[3]
            # get the score
            score = float(line.split()[2])
            # print the score
            avg_score += ( score * (11-j))
    avg_score /= 55
    # get the row index of valid_seq_ids["sequence_global_id"] == i
    row_index = valid_seq_ids[valid_seq_ids["sequence_global_id"] == i].index[0]
    valid_seq_ids.loc[row_index, "avg_score"] = avg_score

# order  the dataframe by avg_score
valid_seq_ids = valid_seq_ids.sort_values(by="avg_score", ascending=True)

# draw run_id against avg_score
import matplotlib.pyplot as plt
plt.scatter(valid_seq_ids["sequence_global_id"], valid_seq_ids["avg_score"])
plt.show()

# delete all rows with avg_score > -150
valid_seq_ids = valid_seq_ids[valid_seq_ids["avg_score"] < -165]
print(valid_seq_ids.describe())

# draw run_id against avg_score
import matplotlib.pyplot as plt
plt.scatter(valid_seq_ids["sequence_global_id"], valid_seq_ids["avg_score"])
plt.show()


# save the dataframe
valid_seq_ids.to_csv("valid_seq_ids.csv", index=False)