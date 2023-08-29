# Protein Structure Modifications


## basic usage for creating reduced structures
in `main.py` define: 
- `run` which is the number of the run ex: `run = 1`
- `res_nums` which is a list of the residue numbers to keep ex: `res_nums = [1, 2, 3, 4, 5]`
- `chain_mode` which is the mode for selecting chains ex: `chain_mode = "X"` for chosing all the cahins or `chain_mode = "A"` for chosing only chain A
- `keep_radius` which is the radius to keep around the selected residues ex: `keep_radius = 50`

the resulting file can be found at `BioPython_modified_structures` directory.


## Resources
I used the following resources to learn how to use Biopython to modify protein structures.
- [official tutorial](http://biopython.org/DIST/docs/tutorial/Tutorial.pdf)
- [official structure FAQ](https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ)
- [useful youtube video](https://www.youtube.com/watch?v=mL8NPpRxgJA)
- [notebook of video](https://nbviewer.org/github/cgoliver/Notebooks/blob/master/COMP_364/L27/L27.ipynb)

I highly doubt these resources are enough to get good enough, but meh I'm not a bioinformatician.

I used the following resources to learn parrallel programming in python.
- [random article](https://www.machinelearningplus.com/python/parallel-processing-python/?expand_article=1)

I used this paper as inspiration for surface detecation.
- [paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2712621/)

## Old steps
1. Download and load protein structures (binder + target).
2. Strip the water molecules and hetero-atoms then save the new structure.
3. Combine the two structures into one, using ChimeraX. (This is done manually)
4. Load the combined structure into Biopython.
5. Reduce the size of the structure.
6. Save the reduced structure.