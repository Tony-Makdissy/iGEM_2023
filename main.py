import BioPython_structure_handling as bpsh
import numpy as np

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    test = bpsh.Protein()
    test.read_structure("2xgf", generate=True)
    # test.peel_structure()

    run = 19
    res_nums = [903, 907, 904, 902]

    chain_mode = "X"
    keep_radius = 50


    hotspots = []
    if chain_mode == "X":
        chains = ["A", "B", "C"]
    else :
        chains = chain_mode

    for let in chains:
        for num in res_nums:
            hotspots.append(test.structure[0][let][num])

    to_keep = []

    for model in test.structure:
        for chain in model:
            for res in chain:
                for spot in hotspots:
                    if np.linalg.norm(res.center_of_mass() - spot.center_of_mass()) <= keep_radius:
                        to_keep.append(res)

    saving_name = f"p01_run{run:02d}_2xgf"
    for num in res_nums:
        # TODO: what if you have several chains!?
        saving_name += f"_{chain_mode}{num}"
    saving_name+=f"_r{keep_radius:02d}"

    test.save_structure(saving_name,
                        selection_class=bpsh.Protein.general_selection_class(residues_to_keep=to_keep))

    print(f"run{run} is done")