# coding: utf-8

from __future__ import division, print_function, unicode_literals, absolute_import

"""
This module defines tasks that support running PWscf.
"""

import os
import subprocess
from fireworks import explicit_serialize, FiretaskBase
from atomate.utils.utils import env_chk, get_logger

logger = get_logger(__name__)


@explicit_serialize
class RunPwscfDirect(FiretaskBase):
    """
    Execute a command directly (no custodian).

    Required params:
        cmd (str): the name of the full executable to run. Supports env_chk.
    Optional params:
        expand_vars (str): Set to true to expand variable names in the cmd.
    """

    required_params = ["pwscf_cmd"]
    optional_params = ["expand_vars"]

    def run_task(self, fw_spec):
        cmd = env_chk(self["pwscf_cmd"], fw_spec)
        if self.get("expand_vars", False):
            cmd = os.path.expandvars(cmd)

        logger.info("Running command: {}".format(cmd))
        return_code = subprocess.call(cmd, shell=True)
        logger.info("Command {} finished running with returncode: {}".format(cmd, return_code))


@explicit_serialize
class RunNoPwscf(FiretaskBase):
    """
    Do NOT run vasp. Do nothing.
    """

    def run_task(self, fw_spec):
        pass
