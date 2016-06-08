#!/usr/bin/python3

from . import tenv
from . import plan
from . import apicall

class PerfTest:
    def __init__(self, suite, cases, tenv):
        self.suite = suite
        self.tenv = tenv
        self.cases = cases
        self.distro = tenv.distro
        self.plan = plan.Run(self.distro)
        self.trpairs = []

    def compare1(self, dynapi, case, trpair):
        endpoint = "/api/report/v1/comparison/run"
        pargs = {}
        pargs["suite"] = self.suite
        pargs["case"] = case
        pargs["q_tenv_id"] = self.tenv.get_id(dynapi)
        pargs["r_tenv_id"] = trpair["tenv_id"]
        pargs["q_run_id"] = self.plan.run_id
        pargs["r_run_id"] = trpair["run_id"]
        return dynapi.get(endpoint, pargs, []).json()["conclusion"]

    def update_conclusion(self, dynapi, case, trpair, conclusion):
        endpoint = "/api/report/v1/status/run"
        pargs = {}
        pargs["suite"] = self.suite
        pargs["case"] = case
        pargs["q_tenv_id"] = self.tenv.get_id(dynapi)
        pargs["r_tenv_id"] = trpair["tenv_id"]
        pargs["q_run_id"] = self.plan.run_id
        pargs["r_run_id"] = trpair["run_id"]
        pargs["status"] = conclusion
        return dynapi.post(endpoint, pargs, None, None).json()

    def complete(self, dynapi):
        if self.trpairs : return
        self.plan.complete(dynapi)
        self.run_id = self.plan.run_id
        for drpair in self.plan.drpairs:
            distro = drpair["distro"]
            run_id = drpair["run_id"]
            r_tenv = tenv.Tenv(distro, self.tenv.component,
                               self.tenv.inst, self.tenv.machine,
                               self.tenv.extra)
            r_tenv_id = r_tenv.get_id(dynapi)
            trpair = {"tenv_id":r_tenv_id, "run_id":run_id}
            self.trpairs.append(trpair)

    def compare(self, dynapi):
        self.complete(dynapi)
        for case in self.cases:
            for trpair in self.trpairs:
                conclusion = self.compare1(dynapi, case, trpair)
                self.update_conclusion(dynapi, case, trpair, conclusion)
