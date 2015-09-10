import sys
import numpy as np
import functools
import logging
from common import *

class DictOfDict(dict):
    def __missing__(self, key):
        self[key] = DictOfDict()
        return self[key]

class Error(Exception):
    pass

class DODError(Error):
    def __init__(self, dod, path):
        self.dod = dod
        self.path = path

def dod_get_leaf_by_path(node, path):
    for name in path:
        try:
            assert(isinstance(node, DictOfDict))
        except AssertionError as e:
            print("path %s" % path)
            raise(e)
        if name in node:
            node = node[name]
        else:
            return None
    return node

def dod_travel_depth(pnode, path):
    for name in pnode:
        path.append(name)
        node = pnode[name]
        if isinstance(node, DictOfDict):
            yield from dod_travel_depth(node, path)
        else:
            yield node #leaf
        path.pop()

def dod_vector_travel_depth(dod_vector, cb_func, cb_data):
    ''' first element is the reference  '''
    path = list()
    ref0 = dod_vector[0]
    others = dod_vector[1:]
    for leaf in dod_travel_depth(ref0, path):
        leaf_list = list()
        leaf_list.append(leaf)
        for dod in others:
            other_leaf = dod_get_leaf_by_path(dod, path)
            if not leaf: raise DODError(dod, path) # return which file dose not exist.
            leaf_list.append(other_leaf)
        cb_func(path, leaf_list, cb_data)

def dod_vector_travel_depth_return_dod(dod_vector, cb_func, cb_data):
    new_dod = DictOfDict()
    def _wrapper(path, leaf_list, cb_data):
        new_leaf = cb_func(path, leaf_list, cb_data)
        node = new_dod
        for name in path[0:-1]:
            node = node[name]
        name = path[-1]
        node[name] = new_leaf
    dod_vector_travel_depth(dod_vector, _wrapper, cb_data)
    return new_dod

class NumberOperator:
    '''
    All these operation on basic num such as int, float.
    '''
    max = max
    min = min
    sum = sum

    @staticmethod
    def mean(vector):
        return np.mean(np.array(vector))

    @staticmethod
    def std(vector):
        return np.std(np.array(vector))

    @staticmethod
    def cov(vector): #covariance
        return np.cov(np.array(vector))

    @staticmethod
    def cv(vector): #coefficient of variation
        return np.std(np.array(vector)) / np.mean(np.array(vector))

    @staticmethod
    def compare(vector):
        ref0 = vector[0]
        ref1 = vector[1]
        if ref1 is None or not ref0:
            ret = float('nan')
        else:
            ret = ref1 / ref0 - 1
        return ret

    @staticmethod
    def compare1(vector):
        ref0 = vector[0]
        ref1 = vector[1]
        if ref1 is None or not ref0:
            ret = float('nan')
        else:
            ret = 1 - ref1 / ref0
        return ret

    @staticmethod
    def is_number(x):
        return isinstance(x, (int, float, complex))

class VectorOperator:
    @staticmethod
    def _call(name, vector):
        ref0 = vector[0]
        if NumberOperator.is_number(ref0):
            stat_func = getattr(NumberOperator, name)
        else:
            stat_func = getattr(ref0, name)
        return stat_func(vector)

    @staticmethod
    def max(vector):
        return VectorOperator._call("max", vector)

    @staticmethod
    def min(vector):
        return VectorOperator._call("min", vector)

    @staticmethod
    def sum(vector):
        return VectorOperator._call("sum", vector)

    @staticmethod
    def mean(vector):
        return VectorOperator._call("mean", vector)

    @staticmethod
    def std(vector):
        return VectorOperator._call("std", vector)

    @staticmethod
    def cov(vector): #covariance
        return VectorOperator._call("cov", vector)

    @staticmethod
    def cv(vector): #coefficient of variation
        return VectorOperator._call("cv", vector)

    @staticmethod
    def compare(vector):
        return VectorOperator._call("compare", vector)

    @staticmethod
    def compare1(vector):
        return VectorOperator._call("compare1", vector)


class StatisticDict(dict):
    @staticmethod
    def compare(vector):
        ref0 = vector[0]
        ref1 = vector[1]
        retd = StatisticDict()
        for k in ref0:
            d0 = ref0[k]
            d1 = ref1[k]
            if d1 is None or not d0:
                retd[k] = float('nan')
            else:
                retd[k] = d1 / d0 - 1
        return retd

    @staticmethod
    def compare1(vector):
        ref0 = vector[0]
        ref1 = vector[1]
        retd = StatisticDict()
        for k in ref0:
            d0 = ref0[k]
            d1 = ref1[k]
            if d1 is None or not d0:
                retd[k] = float('nan')
            else:
                retd[k] = 1 - d1 / d0
        return retd

def dod_vector_operator_simple(func):
    @functools.wraps(func)
    def travel_wrapper(dod_vector):
        return dod_vector_travel_depth_return_dod(dod_vector, func, None)
    return travel_wrapper

class DODOperator:

    '''The Namespace for Operators of NamedTree
    Some of them have only two operands, so they can be implemented
    as a special math method of NamedTree. Some ones have more than two operands.'''

    @staticmethod
    @dod_vector_operator_simple
    def max(path, vector, cb_data):
        return VectorOperator.max(vector)

    @staticmethod
    @dod_vector_operator_simple
    def min(path, vector, cb_data):
        return VectorOperator.min(vector)

    @staticmethod
    @dod_vector_operator_simple
    def sum(path, vector, cb_data):
        return VectorOperator.sum(vector)

    @staticmethod
    @dod_vector_operator_simple
    def mean(path, vector, cb_data):
        return VectorOperator.mean(vector)

    @staticmethod
    @dod_vector_operator_simple
    def std(path, vector, cb_data):
        return VectorOperator.std(vector)

    @staticmethod
    @dod_vector_operator_simple
    def cov(path, vector, cb_data): #covariance
        return VectorOperator.cov(vector)

    @staticmethod
    @dod_vector_operator_simple
    def compare(path, vector, cb_data):
        return VectorOperator.compare(vector)

    @staticmethod
    @dod_vector_operator_simple
    def compare1(path, vector, cb_data):
        return VectorOperator.compare1(vector)

    @staticmethod
    @dod_vector_operator_simple
    def statistic(path, vector, cb_data):
        stat = StatisticDict()
        stat['max'] = VectorOperator.max(vector)
        stat['min'] = VectorOperator.min(vector)
        stat['sum'] = VectorOperator.sum(vector)
        stat['mean'] = VectorOperator.mean(vector)
        stat['std'] = VectorOperator.std(vector)
        #stat['cov'] = VectorOperator.cov(vector)
        stat['cv'] = VectorOperator.cv(vector)
        return stat

class DODLog:
    def __init__(self, stream = None):
        self.stream = stream
        self._dod = DictOfDict()

class DODLogList:
    def __init__(self, stream = None):
        self.stream = stream
        self._dod_list = list()

    def append(self, dod):
        self._dod_list.append(dod)

    def statistic(self):
        return DODOperator.statistic(self._dod_list)

    def compare(self):
        return DODOperator.compare(self._dod_list)

class DODLogStatistic:
    def __init__(self, stream = None):
        self.stream = stream
        self._dod = DictOfDict()

class DODResult:
    '''Deprecated'''
    def __init__(self, dod):
        print("DODResult is deprecated")
        self.dod = dod

class DODGroup(list):
    '''Deprecated'''
    def __init__(self, dod_list, name = "NoName"):
        print("DODResult is deprecated")
        self.name = name
        for dod in dod_list:
            self.append(dod)

    def __getattr__(self, name):
        if hasattr(DODOperator, name):
            op = getattr(DODOperator, name)
            logging.debug('op calling %s' % name)
            return DODResult(op(list(map(lambda D: D.dod, self))))
        else:
            raise AttributeError('object dose not have %s', name)

if __name__ == '__main__':
    print("Test of __travel_depth")
    cnode1 = DictOfDict()
    cnode1['l11'] = 11
    cnode1['l12'] = 12
    cnode2 = DictOfDict()
    cnode2['l13'] = 13
    cnode2['l14'] = 14
    cnode3 = DictOfDict()
    cnode3['l15'] = 15
    cnode3['l16'] = 16
    cnode4 = DictOfDict()
    cnode4['l17'] = 17
    cnode4['l18'] = 18
    cnode21 = DictOfDict()
    cnode21['l21'] = cnode1
    cnode21['l22'] = cnode2
    cnode22 = DictOfDict()
    cnode22['l23'] = cnode3
    cnode22['l24'] = cnode4
    cnode31 = DictOfDict()
    cnode31['l31'] = cnode21
    cnode31['l32'] = cnode22
