# coding: utf-8

from __future__ import absolute_import, division, print_function, \
    unicode_literals

"""
Workflows for PWscf runs.
"""

from fireworks import Workflow
from pymatgen.io.pwscf import PWRelaxSet
from atomate.utils.utils import get_logger
from atomate.pwscf.fireworks import PwscfFW

logger = get_logger(__name__)


# TODO: Handle custom kpoints settings
def get_wf_optimization(structure, name="optimization", pwscf_input_set=None, pwscf_cmd="pw.x -i *.in",
                         pseudo_dir=None, db_file=None, tag="", metadata=None):
    """
    Returns a structure optimization workflow.

    Firework 1 : structural relaxation

    Args:
        structure (Structure): input structure to be optimized and run
        name (str): some appropriate name for the transmuter fireworks.
        pwscf_input_set (DictVaspInputSet): vasp input set.
        pwscf_cmd (str): command to run
        db_file (str): path to file containing the database credentials.
        tag (str): some unique string that will be appended to the names of the fireworks so that
            the data from those tagged fireworks can be queried later during the analysis.
        metadata (dict): meta data

    Returns:
        Workflow
    """
    fws, parents = [], []

    # Structure optimization firework
    pwis_relax = pwscf_input_set or PWRelaxSet(structure, pseudo_dir=pseudo_dir)
    fws = [PwscfFW(structure=structure, pwscf_input_set=pwis_relax, pwscf_cmd=pwscf_cmd,
                      db_file=db_file, name="{} structure optimization".format(tag))]

    wfname = "{}:{}".format(structure.composition.reduced_formula, name)

    return Workflow(fws, name=wfname, metadata=metadata)
