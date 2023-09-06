import BioPython_structure_handling as bpsh
import numpy as np
import json
from Bio.PDB.MMCIF2Dict import MMCIF2Dict
import pandas as pd

def process_run(run_config, original_protein):

    pdbid = run_config["pdbid"]
    sub_target = run_config["sub_target"]
    run = run_config["run"]
    keep_radius = run_config["keep_radius"]
    hotspot = run_config["hotspots_names"]
    AA_range = run_config["AA_range"]


    reduced_structure = bpsh.Protein()



    sphere_centers = []

    saving_name = f"p01_run{run:02d}_{pdbid}_{sub_target}"

    for let, num in hotspot:
        sphere_centers.append(original_protein.structure[0][let][num])

        saving_name += f"_{let}{num}"
    saving_name += f"_r{keep_radius:02d}"

    to_keep = []

    for model in original_protein.structure:
        for chain in model:
            for res in chain:
                for spot in sphere_centers:
                    if np.linalg.norm(res.center_of_mass() - spot.center_of_mass()) <= keep_radius:
                        to_keep.append(res)

    original_protein.save_structure(saving_name,
                          selection_class=bpsh.Protein.general_selection_class(residues_to_keep=to_keep))

    reduced_structure.read_structure(saving_name, reading_directory="BioPython_modified_structures", file_type="pdb")

    #create a string A,B,C .... of the remaining chains
    chains = ""
    for chain in reduced_structure.structure[0]:
        chains += f"{chain.id}:"

    chains+= AA_range

    print(f"run{run} is done")

    return {"run_id":run, "chains":chains}



# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    pdbid = "7vs5"

    # create a pandas dataframe with two coloumns, run and reamining chains
    df = pd.DataFrame(columns=['run', 'chains'])

    # code
    vertex = bpsh.Protein()
    vertex.read_structure(pdbid, generate=True)
    ## I am renaming to be able to save the structure as pdb file
    ## pdb files do not accept chain names longer than 1 char
    rename_dict = {"hj": 'A', "hk": 'B', "hl": 'C', "hm": 'D', "hn": 'E',
                   "ew": 'F', "ex": 'G', "ey": 'H', "fc": 'I', "fh": 'J', "fd": 'K',
                   "ls": 'L', "lu": 'M', "nc": 'N'}

    chains = list(vertex.structure[0].get_chains())
    ## if I don't create a list of chains and delete in the for loop
    ## it will delete the chain and reindex the chains, thus skipping some chains
    for chain in chains:
        if chain.id not in rename_dict.keys():
            vertex.structure[0].detach_child(chain.id)

    for chain in vertex.structure[0]:
        new_id = rename_dict.get(chain.id, chain.id)
        chain.id = new_id

    vertex.save_structure("vertex_structure_renamed",
                          selection_class=bpsh.Protein.general_selection_class())

    # Read the JSON file
    with open('hotspots.json') as f:
        data = json.load(f)
        runs = data["runs"]

    # Process each run
    for run_config in runs:
        row = process_run(run_config, vertex)
        df = df._append(row, ignore_index=True)

    # save the dataframe to a csv file
    df.to_csv(f"runs_{pdbid}.csv", index=False)