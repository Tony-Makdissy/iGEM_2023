import os
import Bio.PDB


# TODO: when you use captial letters for structure names, it will not work! becuse the generated file will be in lower case
# EX: protein.read_structure("7KZF", generate=True)

class Protein:
    """ This class is used to load, save and modify protein structures """

    def __int__(self):
        self.structure = None

    class general_selection_class(Bio.PDB.Select):
        """ This class is used to select models, chains, residues, or atoms from a protein structure """

        def __init__(self, **kwargs):

            list_of_acceptable_keys = []
            for entity in ["models", "chains", "residues", "atoms"]:
                for action in ["to_keep", "to_remove"]:
                    list_of_acceptable_keys.append(f"{entity}_{action}")

            for key in kwargs.keys():
                if key not in list_of_acceptable_keys:
                    raise Exception(f"Unknown argument: {key}")
                # check that to_keep and to_remove are lists
                if key.endswith("to_keep") or key.endswith("to_remove"):
                    if type(kwargs[key]) != list:
                        raise Exception(f"{key} must be a list")

            for entity in ["models", "chains", "residues", "atoms"]:
                kwargs[f"{entity}_to_keep"] = kwargs.get(f"{entity}_to_keep", [])
                kwargs[f"{entity}_to_remove"] = kwargs.get(f"{entity}_to_remove", [])

            self.models_to_keep = kwargs["models_to_keep"]
            self.models_to_remove = kwargs["models_to_remove"]

            self.chains_to_keep = kwargs["chains_to_keep"]
            self.chains_to_remove = kwargs["chains_to_remove"]

            self.residues_to_keep = kwargs["residues_to_keep"]
            self.residues_to_remove = kwargs["residues_to_remove"]

            self.atoms_to_keep = kwargs["atoms_to_keep"]
            self.atoms_to_remove = kwargs["atoms_to_remove"]

            for entity in ["models", "chains", "residues", "atoms"]:
                if kwargs[f"{entity}_to_keep"] != [] and kwargs[f"{entity}_to_remove"] != []:
                    raise Exception(f"Cannot keep and remove {entity} at the same time!")

        def accept_model(self, model):
            if self.models_to_keep == []:
                return model not in self.models_to_remove
            # if models_to_keep & models_to_remove are empty it will return 1

            else:
                return model in self.models_to_keep

        def accept_chain(self, chain):
            if self.chains_to_keep == []:
                return chain not in self.chains_to_remove
            else:
                return chain in self.chains_to_keep

        def accept_residue(self, residue):
            if self.residues_to_keep == []:
                return residue not in self.residues_to_remove
            else:
                return residue in self.residues_to_keep

        def accept_atom(self, atom):
            if self.atoms_to_keep == []:
                return atom not in self.atoms_to_remove
            else:
                return atom in self.atoms_to_keep

    def select_solvent_accessible_residues_and_core(self, probe_radius=1.40, n_points=100, radii_dict=None,
                                                    threshold=100, return_ids=False, shell_or_core="shell"):
        """ This function is used to select solvent accessible residues from a protein structure """
        # I didn't implement the atom, model, and chain selection yet!
        sr = Bio.PDB.ShrakeRupley(probe_radius=probe_radius, n_points=n_points, radii_dict=radii_dict)
        sr.compute(self.structure, level='R')  # “A” (Atom), “R” (Residue), “C” (Chain), “M” (Model), or “S” (Structure)

        shell = []
        core = []
        for residue in self.structure.get_residues():
            if residue.sasa > threshold:
                shell.append(residue)
            else:
                core.append(residue)

        if return_ids:
            shell, core = list(map(lambda x: x.id, shell)), list(map(lambda x: x.id, core))

        if shell_or_core == "shell":
            return shell
        elif shell_or_core == "core":
            return core
        elif shell_or_core == "both":
            return shell, core
        else:
            raise Exception("shell_or_core must be either shell, core, or both")

    # TODO: write a code to save the shit and a code to repeat the saving process
    def peel_structure(self, **kwargs):

        acceptable_args = ["threshold", "probe_radius", "n_points", "radii_dict",
                           "saving_directory"]
        # check the kwargs, if a key not in acceptable_args, raise error
        for key in kwargs.keys():
            if key not in acceptable_args:
                raise NameError(f"we don't have '{key}' as an argument, pal!")

        threshold = kwargs.get("threshold", 50)
        probe_radius = kwargs.get("probe_radius", 1.4)
        n_points = kwargs.get("n_points", 100)
        radii_dict = kwargs.get("radii_dict", None)
        saving_directory = kwargs.get("saving_directory", "protein_peels")

        original_structure = self.structure
        # because I will make changes on the structure

        # check if directory exists "protein_peels", if not create it
        if not os.path.exists(saving_directory):
            os.makedirs(saving_directory)

        index = -1
        while True:
            index += 1
            protein_shell, protein_core = \
                self.select_solvent_accessible_residues_and_core(threshold=threshold, shell_or_core="both",
                                                                 probe_radius=probe_radius, n_points=n_points,
                                                                 radii_dict=radii_dict)

            sel_class = self.general_selection_class(residues_to_keep=protein_shell)
            self.save_structure(f"shell_{index}", saving_directory=saving_directory,
                                selection_class=sel_class, replace=False)

            if protein_core == []:
                break

            sel_class = self.general_selection_class(residues_to_keep=protein_core)
            self.save_structure(f"core_{index}", saving_directory=saving_directory,
                                selection_class=sel_class, replace=True)  # replace=True to update the structure

        self.structure = original_structure  # to return the structure to its original state

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

    # TODO: remove structure_name parameter it makes no sense
    def save_structure(self, structure_name, saving_name=None, saving_directory="BioPython_modified_structures",
                       selection_class=general_selection_class(), replace=False):
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
            # a bool to update the structure after saving
            self.read_structure(saving_name, saving_directory, file_type="pdb")


if __name__ == '__main__':
    target = Protein()
    target.read_structure("7kzf", generate=True)
    # print(target.select_solvent_accessible_residues())
    # for res in target.select_solvent_accessible_residues():
    #     print(res.id)

    # to_keep = list(map(lambda x: x.id, target.select_solvent_accessible_residues(threshold=100)))
    to_keep = target.select_solvent_accessible_residues_and_core()

    target.save_structure("test_1", selection_class=Protein.general_selection_class(residues_to_keep=to_keep))
    # target.peel_structure()
    target.save_structure("test_2", selection_class=Protein.general_selection_class())
