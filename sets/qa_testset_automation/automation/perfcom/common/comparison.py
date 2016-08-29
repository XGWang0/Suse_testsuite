#!/usr/bin/python3

from .error import *
from .debug import *
from . import debug
debug.DEBUG = True
class Comparison:
    def __init__(self, suite, case):
        self.suite = suite
        self.case = case

    def set_q_tenv_id(self, id):
        self.q_tenv_id = id

    def set_r_tenv_ids(self, ids):
        self.r_tenv_ids = ids

    def _p_q_args(self):
        pargs = {}
        pargs["case"] = self.case
        pargs["suite"] = self.suite
        pargs["q_tenv_id"] = self.q_tenv_id;
        pargs["r_tenv_ids"] = self.r_tenv_ids;
        return pargs, {}

    def _get_details(self, dynapi):
        pargs, qargs = self._p_q_args()
        try:
            ret = dynapi.get("/api/report/v1/comparison/plan/id", pargs, qargs).json()
        except HTTPError as e:
            raise NoPlanError(str(e)) from e
        return ret

    def _row(self, question, references):
        stat_keys = ('mean', 'std', 'cv', 'max', 'min')
        for k in question:
            for stat_key in stat_keys:
                v_list = []
                for reference in references:
                    if not k in reference['stat']:
                        v_list.append('NAN')
                    else:
                        v_list.append(reference['stat'][k][stat_key])
                    if not k in reference['comparison']:
                        v_list.append('NAN')
                    else:
                        v_list.append(reference['comparison'][k][stat_key])
                v_list.append(question[k][stat_key])
                if stat_key == 'mean':
                    yield k, stat_key, v_list
                else:
                    yield '', stat_key, v_list

    def page(self, dynapi):
        data = self._get_details(dynapi)
        devlogR_obj(data)
        question = data["question"]
        references = data["references"]
        w_prefix = 0
        w_stat_key = 0
        w_v_list = []
        i = 0
        while i < len(references) * 2:
            w_v_list.append(0)
            i += 1
        w_v_list.append(0)
        for prefix, stat_key, value_list in self._row(question, references):
            w_prefix = max(w_prefix, len(str(prefix)))
            w_stat_key = max(w_stat_key, len(str(stat_key)))
            w_v_list_tmp = []
            i = 0
            while i < len(w_v_list) - 1:
                w_stat = len("{0:.4f}".format(value_list[i]))
                w_comparison = len("{0:.2%}".format(value_list[i+1]))
                w_v_list_tmp.append(max(w_v_list[i], w_stat))
                w_v_list_tmp.append(max(w_v_list[i+1], w_comparison))
                i += 2
            w_stat = len("{0:.4f}".format(value_list[i]))
            w_v_list_tmp.append(max(w_v_list[i], w_stat))
            w_v_list = w_v_list_tmp
        fmt = "{{0:{0}}}\t{{1:{1}}}".format(w_prefix, w_stat_key)
        i = 0
        while i < len(w_v_list) - 1:
            fmt += "\t    {{{0}:{2}.4f}}  {{{1}:{3}.2%}}".format(i+2, i+3, w_v_list[i], w_v_list[i+1])
            i += 2
        fmt += "\t    {{{0}:{1}.4f}}".format(i+2, w_v_list[i])
        for prefix, stat_key, values in self._row(question, references):
            print(fmt.format(prefix, stat_key, *values))

