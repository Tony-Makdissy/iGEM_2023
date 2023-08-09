import pandas as pd
import os
import shutil

# read the csv file
df = pd.read_csv("firs_patch_runs_parameters.csv", index_col="run_id")

# check if a directory exists, if not create it
if not os.path.exists("unpacked_files"):
    os.mkdir("unpacked_files")

zip_dir = "RFdiffusion_finished_runs"
# go over the rows
for index, row in df.iterrows():
    zip_name = zip_dir + "/" + row["zip_name"]
    new_folder_name = zip_dir + "/" + "p00_run" + str(index).zfill(2) # just to get more readable error messages

    # Unzip the file
    os.system("unzip -o " + zip_name + " -d " + new_folder_name)

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
        new_file_name = os.path.join(new_folder_name, "p00_run_" + str(index).zfill(2) + "_" + os.path.basename(file))
        shutil.move(file, new_file_name)


    # remove the directory
    shutil.rmtree(os.path.join(new_folder_name, "outputs"))

# check if a directory exists, if not create it
if not os.path.exists("unpacked_files"):
    os.mkdir("unpacked_files")

# move p00_run* folders to unpacked_files
for item in os.listdir(zip_dir):
    if item.startswith("p00_run"):
        shutil.move(os.path.join(zip_dir, item), "unpacked_files")
