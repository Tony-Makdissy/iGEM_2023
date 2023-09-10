import pandas as pd
import os
import shutil

# check if a directory exists, if not create it
if not os.path.exists("unpacked_files"):
    os.mkdir("unpacked_files")

zip_dir = "finished_runs"
# go over the rows
for zip_file in os.listdir(zip_dir):
    # get the names
    zip_name = zip_dir + "/" + zip_file
    run_id = int(zip_file[7:9])
    new_folder_name = f"{zip_dir}/p01_run{run_id:02d}"

    # Unzip the file
    os.system("unzip -o " + zip_name + " -d " + new_folder_name)


    # meaningfull comment
    list_of_files_to_move = []
    dir_to_unpack = os.path.join(new_folder_name, "outputs")
    for item in os.listdir(dir_to_unpack):
        item_path = os.path.join(dir_to_unpack, item)
        if os.path.isfile(item_path):
            continue
        if item == "traj":
            continue
        dir_to_unpack = item_path
        break

    for item in os.listdir(dir_to_unpack):
        item_path = os.path.join(dir_to_unpack, item)
        if item == "design.fasta" or item == "mpnn_results.csv":
            list_of_files_to_move.append(item_path)
    dir_to_unpack = os.path.join(dir_to_unpack, "all_pdb")
    for item in os.listdir(dir_to_unpack):
        list_of_files_to_move.append(os.path.join(dir_to_unpack, item))

    # move the files to the unpacked_files directory and add the run_id as prefix
    for file in list_of_files_to_move:
        new_file_name = os.path.join(new_folder_name, "p01_run" + str(run_id).zfill(2) + "_" + os.path.basename(file))
        shutil.move(file, new_file_name)

    # remove the directory
    shutil.rmtree(os.path.join(new_folder_name, "outputs"))

# move p01_run* folders to unpacked_files
for item in os.listdir(zip_dir):
    if not item.endswith(".zip"):
        shutil.move(os.path.join(zip_dir, item), "unpacked_files")

# creating a summary file
# read every p01_run*/p01_run*_mpnn_results.csv file and combine them into one dataframe
summary_df = pd.DataFrame()
for item in os.listdir("unpacked_files"):
    if item.startswith("p01_run"):
        csv_name = f"unpacked_files/{item}/{item}_mpnn_results.csv"
        temp_df = pd.read_csv(csv_name)
        temp_df["patch_id"] = int(item[1:3])
        temp_df["run_id"] = int(item[7:9])
        # rename "n" to "sequence_local_id" / design to design_id
        temp_df.rename(columns={"n": "sequence_local_id", "design": "design_id"}, inplace=True)

        # reorder the columns
        cols = ["patch_id", "run_id", "design_id", "sequence_local_id",
                "mpnn", "plddt", "i_ptm", "i_pae", "rmsd", "seq"]
        temp_df = temp_df[cols]

        summary_df = summary_df._append(temp_df)

# sort the dataframe the first column then the second column and so on, for readability and easier comparison
summary_df.sort_values(by=["patch_id", "run_id", "design_id", "sequence_local_id"], inplace=True)
# extract the binder sequence from the sequence column, it's after '/'
summary_df["binder_sequence"] = summary_df["seq"].apply(lambda x: x.split("/")[1])
# reset the index
summary_df.reset_index(drop=True, inplace=True)
# check the distribution of "i_pae"
print(summary_df["i_pae"].describe())

# check if the same "binder_sequence" appears in different rows
print(summary_df["binder_sequence"].describe())
# create a new column called "disregard" and set it to False
summary_df["disregard"] = False
# set the "disregard" column to True to keep only one copy of each "binder_sequence"
summary_df.loc[summary_df.duplicated(subset=["binder_sequence"], keep="first"), "disregard"] = True
# check the distribution of "binder_sequence" after disregarding the duplicates
print(summary_df[summary_df["disregard"] == False]["binder_sequence"].describe())

# save a graph of "i_pae" against "run_id"
fig = summary_df.plot.scatter(x="run_id", y="i_pae", title="i_pae against run_id").get_figure()
fig.savefig("i_pae_against_run_id.png")

# save the dataframe to a csv file
summary_df.to_csv("sequences_summary.csv", index_label="sequence_global_id")
