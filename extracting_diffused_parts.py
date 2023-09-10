import BioPython_structure_handling as bsh
import pandas as pd
import os
import multiprocessing as mp

# check and then create a directory called "HDOCK_docking_scores"
if not os.path.exists("extracted_diffused_parts"):
    os.makedirs("extracted_diffused_parts")


# # create HPV L-1 capsid protein (7kzf), and save it to a file in HDOCK_docking_scores
# t4_long_tail = bsh.Protein()
# t4_long_tail.read_structure("2xgf", generate=True)
# t4_long_tail.save_structure("2xgf",
#                       saving_directory="extracted_diffused_parts")


# read "sequences_summary.csv" and "firs_patch_runs_parameters.csv" into dataframes
sequences_summary = pd.read_csv("sequences_summary.csv")
runs_parameters = pd.read_csv("Parameters_p01.csv")


# iterate over the rows of sequences_summary dataframe each row as dict
for i, row in sequences_summary.iterrows():
    # first create a directory for the docking results in HDOCK_docking_scores of type "seq_id"
    seq_doc_dir = f"extracted_diffused_parts/sequence{row['sequence_global_id']:04d}"
    if not os.path.exists(seq_doc_dir):
        os.makedirs(seq_doc_dir)

    # get the .pdb file dir from the sequences_summary dataframe

    run_id = row["run_id"]
    design_id = row["design_id"]
    sequence_local_id = row["sequence_local_id"]
    sequence_global_id = row["sequence_global_id"]
    pdb_dir = f"unpacked_files/p01_run{run_id:02d}"
    pdb_name = f"p01_run{run_id:02d}_design{design_id}_n{sequence_local_id}"

    # read the .pdb file into a protein object
    complex = bsh.Protein()
    complex.read_structure(structure_name=pdb_name,
                           reading_directory=pdb_dir,
                           file_type="pdb")

    # rename chains
    # I'm renaming the chains, so they wont interfere with full structure
    renames = {
        "A": "Y",
        "B": "Z"
    }
    for model in complex.structure:
        for chain in model:
            old_name = chain.get_id()
            new_name = renames.get(old_name)
            chain.id = new_name

    chains_to_keep = [complex.structure[0]["Z"]]

    # save the .pdb file to the docking directory
    complex.save_structure(structure_name=f"binder{sequence_global_id:04d}",
                           saving_name=f"binder{sequence_global_id:04d}",
                           selection_class=bsh.Protein().general_selection_class(chains_to_keep = chains_to_keep),
                           saving_directory=seq_doc_dir)

    # read "hotspot" value from runs_parameters dataframe
    hotspot = runs_parameters.loc[runs_parameters["run_id"] == run_id]["hotspot"].values[0]
    # strip the hotspot then separate the string using "," as a delimiter
    x_checker = hotspot.strip().split(",")
    hotspot = []
    for item in x_checker:
        if item.startswith("X"):
            suffix = item[1:]
            for let in "ABC":
                hotspot.append(let + suffix)
        else:
            hotspot.append(item)

    # for each item in hotspot, but the last char in the beginning
    for i in range(len(hotspot)):
        hotspot[i] = hotspot[i][1:] + ":" + hotspot[i][0]

    # save the hotspot to a file called "rsite.txt", put each item in a new line
    # but don't put a new line at the end of the file
    with open(f"{seq_doc_dir}/rsite.txt", "w") as f:
        for item in hotspot[:-1]:
            f.write(f"{item}\n")
        f.write(f"{hotspot[-1]}")

