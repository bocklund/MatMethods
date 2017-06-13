# coding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

"""
Defines standardized Fireworks that can be chained easily to perform various
sequences of VASP calculations.
"""

import os
from fireworks import Firework

from pymatgen import Structure
from pymatgen.io.pwscf import PWStaticSet

from atomate.common.firetasks.glue_tasks import PassCalcLocs
from atomate.pwscf.firetasks.run_calc import RunPwscfDirect
from atomate.pwscf.firetasks.write_inputs import WritePwscfFromInput


# TODO: add passing of calculations
# TODO: add a PwscfToDb task
class PwscfFW(Firework):
    def __init__(self, structure, pseudo_dir=None, name='PWscf run', pwscf_input_set=None,
                 pwscf_cmd="pw.x -i *.in", override_default_pwscf_params=None, db_file=None,
                 parents=None, **kwargs):
        """
        Optimize the given structure.

        Args:
            structure (Structure): Input structure.
            pseudo_dir (str): Directory for pseudopotentials. Defaults to $HOME/pseudo, as in PWscf defaults
            name (str): Name for the Firework.
            pwscf_input_set (PWInputSet): input set to use. Defaults to PWStaticSet() if None.
            override_default_pwscf_params (dict): If this is not None, these params are passed to
                the default pwscf_input_set, i.e., PWRelaxSet. This allows one to easily override
                some settings, e.g., control, etc.
            pwscf_cmd (str): Command to run vasp.
            db_file (str): Path to file specifying db credentials to place output parsing.
            parents ([Firework]): Parents of this particular Firework.
            \*\*kwargs: Other kwargs that are passed to Firework.__init__.
        """
        pseudo_dir = pseudo_dir or os.path.expanduser('~/pseudo')
        override_default_pwscf_params = override_default_pwscf_params or {}
        pwscf_input_set = pwscf_input_set or PWStaticSet(structure, **override_default_pwscf_params)

        t = []
        t.append(WritePwscfFromInput(structure=structure, pseudo_dir=pseudo_dir, pwscf_input_set=pwscf_input_set))
        t.append(RunPwscfDirect(pwscf_cmd=pwscf_cmd))
        t.append(PassCalcLocs(name=name))
        super(PwscfFW, self).__init__(t, parents=parents, name="{}-{}".format(structure.composition.reduced_formula, name), **kwargs)

