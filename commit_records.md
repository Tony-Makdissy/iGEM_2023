# Commit Records
This document isn't meant to be a full record of all commits,
but rather some notes I would like to keep track of.

## 2023-07-12
I managed to strip the structure from non-protein residues, using the following code:
```Python
class SelectCriteria(Bio.PDB.Select):
    def accept_residue(self, residue):
        return residue.get_id()[0] == " "
```
I have the modified PDB on the left and the original one on the right. 
I've selected one of the residues that were removed from the structure.
![sdsd](/home/tony/PycharmProjects/iGEM_2023/figures_for_personal_records/12July2023_0.png "WOW")


