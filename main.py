import BioPython_structure_handling as bpsh
import numpy as np

from Bio.PDB.MMCIF2Dict import MMCIF2Dict

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # parameters
    pdbid = "7vs5"
    sub_target = "vertex"
    run = 29
    keep_radius = 40
    hotspots_names = [("A", 242), ("A", 245)]

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

    hotspots = []

    saving_name = f"p01_run{run:02d}_{pdbid}_{sub_target}"

    for let, num in hotspots_names:
        hotspots.append(vertex.structure[0][let][num])

        saving_name += f"_{let}{num}"
    saving_name += f"_r{keep_radius:02d}"

    to_keep = []

    for model in vertex.structure:
        for chain in model:
            for res in chain:
                for spot in hotspots:
                    if np.linalg.norm(res.center_of_mass() - spot.center_of_mass()) <= keep_radius:
                        to_keep.append(res)

    vertex.save_structure(saving_name,
                          selection_class=bpsh.Protein.general_selection_class(residues_to_keep=to_keep))

    print(f"run{run} is done")
