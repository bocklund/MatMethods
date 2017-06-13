# coding: utf-8

from __future__ import division, print_function, unicode_literals, \
    absolute_import

"""
This module defines tasks for writing PWscf input sets for various types of PWscf calculations
"""

from fireworks import FiretaskBase, explicit_serialize
from atomate.utils.utils import load_class

# TODO: Handle transmuted structures
# TODO: Handle Write*PwscfFromPrev
@explicit_serialize
class WritePwscfFromInput(FiretaskBase):
    """
    Create VASP input files using implementations of pymatgen's AbstractVaspInputSet. An input set
    can be provided as an object or as a String/parameter combo.

    Required params:
        structure (Structure): structure
        pwscf_input_set (PWInput or str): Either a PWInput object or a string
            name for the PWscf input set (e.g., "PWRelaxSet").

    Optional params:
        pwscf_input_params (dict): When using a string name for PWscf input set, use this as a dict
            to specify kwargs for instantiating the input set parameters. For example, if you want
            to change the control settings, you should provide: {"control": ...}.
            This setting is ignored if you provide the full object representation of a PWInput
            rather than a String.
    """

    required_params = ["structure", "pwscf_input_set"]
    optional_params = ["pseudo_dir", "pwscf_input_params"]

    def run_task(self, fw_spec):
        # if a full PWInput object was provided
        if hasattr(self['pwscf_input_set'], 'write_input'):
            pwis = self['pwscf_input_set']

        # if PWInput String + parameters was provided
        else:
            pwis_cls = load_class("pymatgen.io.pwscf",
                                 self["pwscf_input_set"])
            pwis = pwis_cls(self["structure"], self["pseudo_dir"]
                          **self.get("pwscf_input_params", {}))
        pwis.write_input(".")
