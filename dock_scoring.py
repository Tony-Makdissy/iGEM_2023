import stripping_protein as sp
import pandas as pd
import os
import multiprocessing as mp

# check and then create a directory called "HDOCK_docking_scores"
if not os.path.exists("HDOCK_docking_scores"):
    os.makedirs("HDOCK_docking_scores")

# create HPV L-1 capsid protein (7kzf), and save it to a file in HDOCK_docking_scores
hpv_l1 = sp.Protein()
hpv_l1.read_structure("7kzf", generate=True)

hpv_l1.save_structure("7kzf",
                      saving_name="7kzf_full_structure",
                      selection_class=sp.default_saving_criteria(),
                      saving_directory="HDOCK_docking_scores")

# read "sequences_summary.csv" and "firs_patch_runs_parameters.csv" into dataframes
sequences_summary = pd.read_csv("sequences_summary.csv")
runs_parameters = pd.read_csv("first_patch_runs_parameters.csv")

# save the current working directory
project_wd = os.getcwd()


# create a function that takes an integer which is sequence_global_id and runs the docking
def dock(seq_id, doc_spacing=2.4, doc_angle=30):
    global sequences_summary
    global runs_parameters

    # first create a directory for the docking results in HDOCK_docking_scores of type "seq_id"
    seq_doc_dir = f"HDOCK_docking_scores/sequence{seq_id:04d}"
    if not os.path.exists(seq_doc_dir):
        os.makedirs(seq_doc_dir)

    # get the .pdb file dir from the sequences_summary dataframe
    run_id = sequences_summary.loc[sequences_summary["sequence_global_id"] == seq_id]["run_id"].values[0]
    design_id = sequences_summary.loc[sequences_summary["sequence_global_id"] == seq_id]["design_id"].values[0]
    sequence_local_id = \
        sequences_summary.loc[sequences_summary["sequence_global_id"] == seq_id]["sequence_local_id"].values[0]
    pdb_dir = f"unpacked_files/p00_run{run_id:02d}"
    # don't to exclude .pdb from the end of the file name
    pdb_name = f"p00_run{run_id:02d}_design{design_id}_n{sequence_local_id}"

    # read the .pdb file into a protein object
    complex = sp.Protein()
    complex.read_structure(structure_name=pdb_name,
                           reading_directory=pdb_dir,
                           file_type="pdb")

    # rename chains
    renames = {
        "A": "Y",
        "B": "Z"
    }
    for model in complex.structure:
        for chain in model:
            old_name = chain.get_id()
            new_name = renames.get(old_name)
            chain.id = new_name

    # save the .pdb file to the docking directory
    complex.save_structure(structure_name=f"binder{seq_id:04d}",
                           saving_name=f"binder{seq_id:04d}",
                           selection_class=sp.pick_chain(chain_id="Z"),
                           saving_directory=seq_doc_dir)

    # change the working directory to the docking directory
    os.chdir(seq_doc_dir)

    # read "hotspot" value from runs_parameters dataframe
    hotspot = runs_parameters.loc[runs_parameters["run_id"] == run_id]["hotspot"].values[0]
    # strip the hotspot then separate the string using "," as a delimiter
    hotspot = hotspot.strip().split(",")
    # for each item in hotspot, but the last char in the beginning
    for i in range(len(hotspot)):
        hotspot[i] = hotspot[i][1:] + ":" + hotspot[i][0]

    # save the hotspot to a file called "rsite.txt", put each item in a new line
    # but don't put a new line at the end of the file
    with open("rsite.txt", "w") as f:
        for item in hotspot[:-1]:
            f.write(f"{item}\n")
        f.write(f"{hotspot[-1]}")

    # HDOCK has two separate steps; first it runs the docking, then showing the results
    hdock_command = f"{project_wd}/HDOCKlite-v1.1/hdock ../7kzf_full_structure.pdb binder{seq_id:04d}.pdb" \
                    f" -spacing {doc_spacing} -angle {doc_angle} -rsite rsite.txt -out Hdock.out"\
                    f" > /dev/null 2>&1"  # Redirect output and errors to a null device

    # createpl_command = f"{project_wd}/HDOCKlite-v1.1/createpl Hdock.out complex{seq_id:04d}.pdb" \
    #                    f" -complex -rsite rsite.txt" \
    #                    f" > /dev/null 2>&1"  # Redirect output and errors to a null device

    # run the docking
    os.system(hdock_command)
    # os.system(createpl_command)

    # go back to the project directory
    os.chdir(project_wd)


valid_seq_ids = sequences_summary[sequences_summary["disregard"] == False]
valid_seq_ids = list(valid_seq_ids["sequence_global_id"])

exit()

# create a pool of 3 processes
pool = mp.Pool(processes=2)
# map the dock function to the sequence_global_id column of sequences_summary dataframe
pool.map_async(dock, valid_seq_ids)
# close the pool
pool.close()
# wait for the processes to finish
pool.join()

# dock(seq_id=i, doc_spacing=0.6, doc_angle=5)
