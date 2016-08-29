#!/usr/bin/python3

import logging
logger = logging.getLogger()
from . import tenv
from . import apicall
from .error import *

class PerfTest:
    def __init__(self, suite, cases, tenv, plan):
        self.suite = suite
        self.tenv = tenv
        self.cases = cases
        self.distro = tenv.distro
        self.plan = plan
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
        return dynapi.post_no_body(endpoint, pargs, [], [])

    def complete(self, dynapi):
        if self.trpairs : return
        self.run_id = self.plan.run_id
        self.plan.references(dynapi)
        for drpair in self.plan.drpairs:
            distro = drpair["distro"]
            run_id = drpair["run_id"]
            try:
                r_tenv = tenv.Tenv(distro, self.tenv.component,
                                   self.tenv.inst, self.tenv.machine,
                                   self.tenv.extra)
                r_tenv_id = r_tenv.get_id(dynapi)
            except HTTPError as e:
                logger.error(str(e))
                continue
            trpair = {"tenv_id":r_tenv_id, "run_id":run_id}
            self.trpairs.append(trpair)

    def compare(self, dynapi):
        self.complete(dynapi)
        for case in self.cases:
            for trpair in self.trpairs:
                try:
                    conclusion = self.compare1(dynapi, case, trpair)
                    self.update_conclusion(dynapi, case, trpair, conclusion)
                except HTTPError as e:
                    logger.error(str(e))
