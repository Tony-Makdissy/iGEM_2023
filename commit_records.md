# Commit Records
This document isn't meant to be a full record of all commits,
but rather some notes I would like to keep track of.

## 2023-07-12
I managed to strip the structure from non-protein residues, using the following code:
```Python
class strip_protein(Bio.PDB.Select):
    def accept_residue(self, residue):
        return residue.get_id()[0] == " "
```
I have the modified PDB on the left and the original one on the right. 
I've selected one of the residues that were removed from the structure.
![](/home/tony/PycharmProjects/iGEM_2023/figures_for_personal_records/12July2023_0.png "WOW")

## 2023-07-13
After combining the two structures (binder + target), I loaded the combined structure into Biopython.

I then reduced the size of the structure, using the following code:
```Python
class reduce_protein(Bio.PDB.Select):
    def accept_residue(self, residue):
        diffusion_radius = 50
        distances = np.linalg.norm(diffused_residues_coordinates - residue.center_of_mass(), axis=1)
        return np.any(distances <= diffusion_radius)
```

diffused_residues_coordinates is a numpy array of the coordinates of the residues that were diffused.

and here are screenshots of the result:

![](/home/tony/PycharmProjects/iGEM_2023/figures_for_personal_records/13July2023_0.png) ![](/home/tony/PycharmProjects/iGEM_2023/figures_for_personal_records/13July2023_1.png) ![](/home/tony/PycharmProjects/iGEM_2023/figures_for_personal_records/13July2023_2.png)