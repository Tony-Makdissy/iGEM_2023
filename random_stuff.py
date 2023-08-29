# https://biopython.org/docs/dev/api/Bio.PDB.html
# https://biopython.org/docs/dev/api/Bio.PDB.SASA.html

# print(Bio.PDB.SASA.ATOMIC_RADII) used in ShrakeRupley SASA calculation

import BioPython_structure_handling as bph
import Bio.PDB
import os

# check if directory exists, if not create it
if not os.path.exists("protein_peels"):
    os.makedirs("protein_peels")

protein = bph.Protein()
protein.read_structure("7kzf", generate=True)

structure = protein.structure
sr = Bio.PDB.ShrakeRupley()

sr.compute(structure, level="R")
# print(structure.sasa)
for model in structure:
    for chain in model:
        # print(chain.sasa)
        for residue in chain:
           print(residue.sasa)
        break