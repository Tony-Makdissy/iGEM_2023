class parameters():
    def __init__(self, **kwargs):
        self.patch_id = kwargs.get("patch_id", None)
        self.run_id = kwargs.get("run_id", None)
        self.job_name = kwargs.get("job_name", None)
        self.contigs = kwargs.get("contigs", None)
        self.pdb = kwargs.get("pdb", None)
        self.iterations = kwargs.get("iterations", None)
        self.hotspots = kwargs.get("hotspots", None)
        self.num_designs = kwargs.get("num_designs", None)
        self.num_seqs = kwargs.get("num_seqs", None)
        self.initial_guess = kwargs.get("initial_guess", None)
        self.num_recycles = kwargs.get("num_recycles", None)
        self.use_multimer = kwargs.get("use_multimer", None)
        self.rm_aa = kwargs.get("rm_aa", None)
        self.mpnn_sampling_temp = kwargs.get("mpnn_sampling_temp", None)

        # TODO: create a shorter way to write this
        # TODO: give some default values
        # TODO: read a log csv that has the pathc_id in its name and pick the id automatically
        # TODO: ma