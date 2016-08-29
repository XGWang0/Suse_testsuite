#!/usr/bin/python

from . import tenv
from .error import *

class Run:
    def __init__(self, distro, run_id):
        self.distro = distro
        self.run_id = run_id
        self.drpairs = []

    def _p_q_args(self):
        pargs = {}
        pargs["arch"] = self.distro.arch
        pargs["release"] = self.distro.release
        pargs["build"] = self.distro.build
        pargs["kernel"] = self.distro.kernel
        pargs["run_id"] = self.run_id
        return pargs, {}

    def new_run(self, dynapi):
        jargs = {"distro":self.distro.todict(), "run_id":self.run_id}
        print(jargs)
        try:
            ret = dynapi.post("/api/report/v1/plan/run/new", {}, {}, jargs).json()
        except HTTPError:
            raise

    def references(self, dynapi):
        if self.drpairs: return
        pargs, qargs = self._p_q_args()
        try:
            ret = dynapi.get("/api/report/v1/plan/distropair/references", pargs, qargs).json()
        except HTTPError as e:
            raise NoPlanError(str(e)) from e
        for r_distro in ret["reference"]:
            distro = tenv.OSDistro(self.distro.arch, r_distro["r_release"],
                                   r_distro["r_build"], r_distro["r_kernel"])
            drpair = {"distro": distro, "run_id":r_distro["r_run_id"]}
            self.drpairs.append(drpair)

    def save_pair(self, dynapi, reference_distro, reference_run_id):
        question = {"arch": self.distro.arch, "release":self.distro.release,
                    "build": self.distro.build, "kernel":self.distro.kernel,
                    "run_id": self.run_id}

        reference = {"arch":self.distro.arch, "release": reference_distro.release,
                     "build": reference_distro.build, "kernel":reference_distro.kernel,
                     "run_id": reference_run_id}

        body = {"question":question, "reference":reference}
        pargs = {"arch": self.distro.arch}
        ret = dynapi.post("/api/report/v1/plan/distropair/new", pargs, {}, body)


def new_pair(dynapi, q_distro_run_id, r_distro_run_id):
    pargs = {"question-id":q_distro_run_id, "reference-id":r_distro_run_id}
    try:
        ret = dynapi.post_no_body("/api/report/v1/plan/distropair/new", pargs, {}, {})
    except HTTPError:
        raise

def pair_default_set(dynapi, distro_run_id):
    pargs = {"distro_run_id":distro_run_id}
    try:
        ret = dynapi.post("/api/report/v1/plan/distropair/default/set", pargs, {}, {}).json()
    except HTTPError:
        raise
