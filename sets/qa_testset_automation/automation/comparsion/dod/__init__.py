import sys
import numpy as np
import functools
import logging
from common import *

__all__ = ['DictOfDict', 'DODGroup', 'DODError', 'DODLog', 'DODResult']

class DictOfDict(dict):
    def __missing__(self, key):
        self[key] = DictOfDict()
        return self[key]

class DODError(Error):
    def __init__(self, dod, path):
        self.dod = dod
        self.path = path

def dod_get_leaf_by_path(node, path):
    for name in path:
        assert(isinstance(node, DictOfDict))
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
    print('dod_vector_travel_depth_return_dod')
    def _wrapper(path, leaf_list, cb_data):
        new_leaf = cb_func(path, leaf_list, cb_data)
        node = new_dod
        for name in path[0:-1]:
            node = node[name]
        name = path[-1]
        node[name] = new_leaf
    dod_vector_travel_depth(dod_vector, _wrapper, cb_data)
    return new_dod

def dod_vector_operator_simple(func):
    @functools.wraps(func)
    def travel_wrapper(dod_vector):
        return dod_vector_travel_depth_return_dod(dod_vector, func, None)
    return travel_wrapper

class defaultStatistic:
    #def max
    #def min
    #def sum
    def mean(vector):
        return np.mean(np.array(vector))
    def std(vector):
        return np.std(np.array(vector))
    def cov(vector):
        return np.cov(np.array(vector))
    def ref0_percent(leaf_list):
        ret = list()
        for leaf in leaf_list[1:]:
            ret.append(leaf / ref0)
        return ret

statFuncs = {'max':max, 'min':min, 'sum':sum,
             'mean':defaultStatistic.mean, 'std':defaultStatistic.std,
             'cov':defaultStatistic.cov, 'ref0_percent':defaultStatistic.ref0_percent}

def stat_result_operator(statname):
    def decorator(func):
        @functools.wraps(func)
        def wapper(vector):
            stat_func = statFuncs[statname]
            return stat_func(vector)
        return wapper
    return decorator

class dodStatistic(dict):
    @staticmethod
    @stat_result_operator('max')
    def max(vector): pass

    @staticmethod
    @stat_result_operator('min')
    def min(vector): pass

    @staticmethod
    @stat_result_operator('sum')
    def sum(vector): pass

    @staticmethod
    @stat_result_operator('mean')
    def mean(vector): pass

    @staticmethod
    @stat_result_operator('std')
    def std(vector): pass

    @staticmethod
    @stat_result_operator('cov')
    def cov(vector): pass

    @staticmethod
    @stat_result_operator('ref0_percent')
    def ref0_percent(vector): pass

def dod_statistic_operator(statname):
    def decorator(func):
        def wrapper(path, vector, cb_data):
            ref0 = vector[0]
            if hasattr(ref0, statname):
                stat_func = getattr(ref0, statname)
            else:
                stat_func = statFuncs[statname]
            stat_func(vector)
        return wrapper
    return decorator

class DODOperator:

    '''The Namespace for Operators of NamedTree
    Some of them have only two operands, so they can be implemented
    as a special math method of NamedTree. Some ones have more than two operands.'''

    @staticmethod
    @dod_vector_operator_simple
    @dod_statistic_operator('max')
    def max(vector): pass

    @staticmethod
    @dod_vector_operator_simple
    @dod_statistic_operator('min')
    def min(vector): pass

    @staticmethod
    @dod_vector_operator_simple
    @dod_statistic_operator('sum')
    def sum(vector): pass

    @staticmethod
    @dod_vector_operator_simple
    @dod_statistic_operator('mean')
    def mean(vector): pass

    @staticmethod
    @dod_vector_operator_simple
    @dod_statistic_operator('std')
    def std(vector): pass

    @staticmethod
    @dod_vector_operator_simple
    @dod_statistic_operator('cov')
    def cov(vector): pass

    @staticmethod
    @dod_vector_operator_simple
    @dod_statistic_operator('ref0_percent')
    def ref0_percent(vector): pass

    @staticmethod
    @dod_vector_operator_simple
    def statistic(path, leaf_list, cb_data):
        stat = dodStatistic()
        stat['max'] = dodStatistic.max(leaf_list)
        stat['min'] = dodStatistic.min(leaf_list)
        stat['sum'] = dodStatistic.sum(leaf_list)
        stat['mean'] = dodStatistic.mean(leaf_list)
        stat['std'] = dodStatistic.std(leaf_list)
        stat['cov'] = dodStatistic.cov(leaf_list)
        return stat

    @staticmethod
    @dod_vector_operator_simple
    def example(path, leaf_list, cb_data):
        raise NotImplementedError()

class DODLog(DictOfDict):
    def __init__(self, stream):
        self.stream = stream
        self._dod = DictOfDict()

class DODResult(DictOfDict):
    def __init__(self, dod):
        self.dod = dod

class DODGroup(list):
    def __init__(self, dod_list, name = "NoName"):
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

