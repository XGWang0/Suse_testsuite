#!/usr/bin/python

from . import tenv
from .error import *

class Run:
    def __init__(self, distro, run_id = None):
        self.distro = distro
        self.run_id = run_id
        self.drpairs = []

    def _p_q_args(self):
        pargs = {}
        pargs["arch"] = self.distro.arch
        pargs["release"] = self.distro.release
        pargs["build"] = self.distro.build
        pargs["kernel"] = self.distro.kernel
        return pargs, {}

    def complete(self, dynapi):
        if self.drpairs: return
        pargs, qargs = self._p_q_args()
        try:
            ret = dynapi.get("/api/report/v1/plan/distropair/references_incomplete", pargs, qargs).json()
        except HTTPError as e:
            raise NoPlanError(str(e)) from e
        if not pargs["kernel"] == self.distro.kernel:
            raise ErrorRuntime("kernel version miss matched")
        self.run_id = ret["run_id"]
        for r_distro in ret["reference"]:
            distro = tenv.OSDistro(self.distro.arch, r_distro["r_release"],
                                   r_distro["r_build"], r_distro["r_kernel"])
            drpair = {"distro": distro, "run_id":r_distro["r_run_id"]}
            self.drpairs.append(drpair)

    def get_run_id(self, dynapi):
        if self.run_id: return self.run_id
        (pargs, qargs) = self._p_q_args()
        ret = dynapi.get("/api/report/v1/plan/distropair/run-id", pargs, qargs).json()
        return ret["run_id"]

    def save_pair(self, dynapi, reference_distro, reference_run_id):
        question = {"run_id": self.run_id, "release":self.distro.release,
                    "build": self.distro.build, "kernel":self.distro.kernel}

        reference = {"run_id": reference_run_id, "release": reference_distro.release,
                     "build": reference_distro.build, "kernel":reference_distro.kernel}

        body = {"question":question, "reference":reference}
        pargs = {"arch": self.distro.arch}
        ret = dynapi.post("/api/report/v1/plan/distropair", pargs, {}, body)

