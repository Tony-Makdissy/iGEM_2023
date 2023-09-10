# read files in the directory digital_ocean_2
import os
import pandas as pd

# read sequences_summary.csv as pd data frame
summary = pd.read_csv("sequences_summary.csv")

# create a data frame with the following columns: run_id, score0, score1, score2, score3, score4, score5, score6, score7, score8, score9
df = pd.DataFrame(columns=["sequence_global_id", "score0", "score1", "score2", "score3", "score4", "score5", "score6", "score7", "score8", "score9", "universal_score"])
for item in os.listdir("digital_ocean_2"):
    if item.startswith("Hdock"):
        row = {"sequence_global_id": item[6:-4]}
        # read lines 6 to 16 in item
        with open(f"digital_ocean_2/{item}", "r") as f:
            lines = f.readlines()[5:15]
            # create a list of words
            lines = list(map(lambda x: x.split()[6], lines))
        universal_score = 0
        for i, score in enumerate(lines):
            row[f"score{i}"] = score
            universal_score += (10-i) * float(score)
        row["universal_score"] = float(universal_score)/55.0
        df = df._append(row, ignore_index=True)

# save the data frame as a csv file
df.to_csv("hdock_scores.csv", index=False)

# summary["sequence_global_id"] = summary["sequence_global_id"].astype(int)
df["sequence_global_id"] = df["sequence_global_id"].astype(int)

# merge the two data frames using sequence_global_id as the key
merged = pd.merge(summary, df, on="sequence_global_id")
merged.to_csv("docking_score_with_summary.csv", index=False)