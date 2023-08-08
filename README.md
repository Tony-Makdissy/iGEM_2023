# Protein Structure Modifications

## Resources
I used the following resources to learn how to use Biopython to modify protein structures.
- [official tutorial](http://biopython.org/DIST/docs/tutorial/Tutorial.pdf)
- [official structure FAQ](https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ)
- [useful youtube video](https://www.youtube.com/watch?v=mL8NPpRxgJA)
- [notebook of video](https://nbviewer.org/github/cgoliver/Notebooks/blob/master/COMP_364/L27/L27.ipynb)

I highly doubt these resources are enough to get good enough, but meh I'm not a bioinformatician.

I used the following resources to learn parrallel programming in python.
- [random article](https://www.machinelearningplus.com/python/parallel-processing-python/?expand_article=1)

## Old steps
1. Download and load protein structures (binder + target).
2. Strip the water molecules and hetero-atoms then save the new structure.
3. Combine the two structures into one, using ChimeraX. (This is done manually)
4. Load the combined structure into Biopython.
5. Reduce the size of the structure.
6. Save the reduced structure.