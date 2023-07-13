import os
import numpy as np
import Bio.PDB


class strip_protein(Bio.PDB.Select):
    """
    This class is used to strip the protein from all the water & hetero-atoms
    """
    def accept_residue(self, residue):
        # water and hetero-atoms are named noted as W and H.
        # other residues are named with a space
        return residue.get_id()[0] == " "



diffused_residues_coordinates = None  # to be changed later (step 5)


class reduce_protein(Bio.PDB.Select):
    """
    This class is used to reduce the size of the protein to the residues that are within a certain distance from the
    residues that are to be diffused
    """
    def accept_residue(self, residue):
        diffusion_radius = 50
        distances = np.linalg.norm(diffused_residues_coordinates - residue.center_of_mass(), axis=1)
        # diffused_residues_coordinates is defined as a global variable, but it is not initialized on step 5
        return np.any(distances <= diffusion_radius)


class default_saving_criteria(Bio.PDB.Select):
    """ This class is used to save the whole protein """
    def accept_model(self, model):
        return 1

    def accept_chain(self, chain):
        return 1

    def accept_residue(self, residue):
        return 1

    def accept_atom(self, atom):
        return 1


class Protein:
    """ This class is used to load, save and modify protein structures """
    def __int__(self):
        self.structure = None

    def generate_structure(self, pdb_id, directory="PDB"):
        """ This function is used to download a protein structure from the PDB database """
        pdbl = Bio.PDB.PDBList()
        pdbl.retrieve_pdb_file(pdb_id, pdir=directory)

    def read_structure(self, structure_name, reading_directory='', generate=False, generate_directory="PDB",
                       file_type="cif"):
        """ This function is used to read a protein structure from a file or from the PDB database"""
        if generate:
            reading_directory = generate_directory
            self.generate_structure(structure_name, generate_directory)
        if file_type == "cif":
            parser = Bio.PDB.MMCIFParser()
        elif file_type == "pdb":
            parser = Bio.PDB.PDBParser(PERMISSIVE=1)
        else:
            raise Exception("Dude, what file type is this?")

        self.structure = parser.get_structure(structure_name, f"{reading_directory}/{structure_name}.{file_type}")

    def save_structure(self, structure_name, saving_name=None, saving_directory="BioPython_modified_structures",
                       selection_class=default_saving_criteria(), replace=False):
        """ This function is used to save a protein structure to a file """
        if saving_name is None:
            saving_name = structure_name
        # check if directory exists, if not create it
        if not os.path.exists(saving_directory):
            os.makedirs(saving_directory)

        io = Bio.PDB.PDBIO()
        io.set_structure(self.structure)
        io.save(f"{saving_directory}/{saving_name}.pdb", selection_class)

        if replace:
            self.read_structure(saving_name, saving_directory, file_type="pdb")


if __name__ == '__main__':
    # step 1: load protein structures
    binder = Protein()
    binder.read_structure("3ujz", generate=True)

    target = Protein()
    target.read_structure("7kzf", generate=True)

    # step 2: strip proteins and save them
    binder.save_structure("3ujz", selection_class=strip_protein(), saving_directory="step_2")
    target.save_structure("7kzf", selection_class=strip_protein(), saving_directory="step_2")


    # step 3: combine proteins in a single file
    """" this step is done "manually" in ChimeraX, by loading the two proteins and then saving them in a single file """
    # the part to be diffused is G:804-898
    to_be_diffused = list(range(804, 899))

    # step 4: load the combined protein
    combined = Protein()
    combined.read_structure("combined_7kzf_3ujz", generate=False, reading_directory="step_3", file_type="pdb")
    combined.save_structure("combined_7kzf_3ujz_after_reading", saving_directory="step_4", replace=True)

    # step 5: reduce the size of combined protein
    diffused_residues = combined.structure[0]["G"].child_list
    diffused_residues = [i for i in diffused_residues if i.get_id()[1] in to_be_diffused]
    diffused_residues_coordinates = np.array([i.center_of_mass() for i in diffused_residues])
    # "diffused_residues_coordinates" is defined as a global variable

    # get the maximum and minimum coordinates
    # max_coordinates = np.max(diffused_residues_coordinates, axis=0)
    # min_coordinates = np.min(diffused_residues_coordinates, axis=0)
    # diffused_residues_radius = np.linalg.norm(max_coordinates - min_coordinates)

    # step 6: save the reduced protein
    combined.save_structure("combined_7kzf_3ujz_after_reducing", selection_class=reduce_protein(), saving_directory="step_6")

