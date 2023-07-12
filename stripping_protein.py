# tutorials ..
# official: http://biopython.org/DIST/docs/tutorial/Tutorial.pdf
# official structure FAQ: https://biopython.org/wiki/The_Biopython_Structural_Bioinformatics_FAQ
# useful youtube video: https://www.youtube.com/watch?v=mL8NPpRxgJA
# notebook of video: https://nbviewer.org/github/cgoliver/Notebooks/blob/master/COMP_364/L27/L27.ipynb
import os
import Bio.PDB


class Protein:
    def __int__(self):
        self.structure = None

    def generate_structure(self, pdb_id, directory="PDB"):
        pdbl = Bio.PDB.PDBList()
        pdbl.retrieve_pdb_file(pdb_id, pdir=directory)

    def read_structure(self, structure_name, directory='', generate=False, generate_directory="PDB"):
        if generate:
            directory = generate_directory
            self.generate_structure(structure_name, directory)
        parser = Bio.PDB.MMCIFParser()
        self.structure = parser.get_structure(structure_name, f"{directory}/{structure_name}.cif")

    def save_structure(self, structure_name, saving_name=None, saving_directory="BioPython_modified_structures",
                       selection_class=None):
        if saving_name is None:
            saving_name = structure_name
        # check if directory exists, if not create it
        if not os.path.exists(saving_directory):
            os.makedirs(saving_directory)

        io = Bio.PDB.PDBIO()
        io.set_structure(self.structure)
        io.save(f"{saving_directory}/{saving_name}.pdb", selection_class)


class SelectCriteria(Bio.PDB.Select):
    def accept_model(self, model):
        return 1

    def accept_chain(self, chain):
        return 1

    def accept_residue(self, residue):
        return residue.get_id()[0] == " "

    def accept_atom(self, atom):
        return 1

if __name__ == '__main__':
    protein = Protein()
    protein.read_structure("3ujz", generate=True)
    protein.save_structure("3ujz", selection_class=SelectCriteria())

    # for model in protein.structure:
    #     for chain in model:
    #         for residue in chain:
    #             if residue.get_id()[0] != " ":
    #                 print(residue.get_id())
    print("done")
