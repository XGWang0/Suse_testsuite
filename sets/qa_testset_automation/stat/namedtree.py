import sys
from collections import OrderedDict, Set
import logging

__all__ = ['NamedTree', 'NamedTreeGroup', 'OP_KIND_LEAF', 'OP_KIND_DIR']

log = logging.getLogger()

def _get_key_set(t_list):
    key_uset = set()
    for l in t_list:
        key_uset |= l.keys()

    key_iset = key_uset
    for l in t_list:
        key_iset &= l.keys()

    key_dset = key_uset - key_iset
    return key_uset, key_iset, key_dset

(CHK_OK, CHK_NO_ITEM, CHK_NOT_DICT) = list(range(0,3))
def _check_key(k, t_list, i_list, error):
    iter_t = iter(t_list)
    iter_i = iter(i_list)
    _list = []
    while True:
        try:
            t = next(iter_t)
            i = next(iter_i)
            if k not in t:
                _list.append(i)
        except StopIteration:
            break

    if len(_list) == 0:
        # Do not touch error
        return True
    else:
        error[0], error[1] = (CHK_NO_ITEM, _list)
        return False

def _check_dir(k, t_list, i_list, error):
    iter_t = iter(t_list)
    iter_i = iter(i_list)
    _list = []
    while True:
        try:
            t = next(iter_t)
            i = next(iter_i)
            if not isinstance(t[k], dict):
                _list.append(i)
        except StopIteration:
            break

    if len(_list) == 0:
        # Do not touch error
        return True
    else:
        error[0], error[1] = (CHK_NOT_DICT, _list)
        return False

def _check_file(k, t_list, i_list, error):
    iter_t = iter(t_list)
    iter_i = iter(i_list)
    _list = []
    while True:
        try:
            t = next(iter_t)
            i = next(iter_i)
            if isinstance(t[k], dict):
                _list.append(i)
        except StopIteration:
            break

    if len(_list) == 0:
        # Do not touch error
        return True
    else:
        error[0], error[1] = (CHK_NOT_DICT, _list)
        return False

def named_tree_get_common(t_list, i_list):
    ''' Get the common structure of a list of named_tree
    i_info should be iteratable and each one is for each tree
    each info should have the name property for debug'''
    stack = []
    path = []
    error = [CHK_OK, None]

    key_uset, key_iset, key_dset = _get_key_set(t_list)
    key_uset = sorted(key_uset)
    root_node = OrderedDict()
    for e in key_uset:
        root_node[e] = None
    t_spec = root_node
    iter_iset = iter(key_iset)

    while True:
        try:
            k = next(iter_iset)
        except StopIteration:
            if len(stack) == 0:
                break
            else:
                si = stack.pop()
                (t_list, t_spec, iter_iset) = si
                path.pop()
        else:
            if _check_dir(k, t_list, i_list, error):
                si = (t_list, t_spec, iter_iset)
                stack.append(si)
                path.append(str(k))
                t_list = list(map(lambda d:d[k], t_list))
                key_uset, key_iset, key_dset = _get_key_set(t_list)
                key_uset = sorted(key_uset)
                new_node = OrderedDict()
                for e in key_uset:
                    new_node[e] = None
                t_spec[k] = new_node
                t_spec = new_node
                iter_iset = iter(key_iset)
            elif _check_file(k, t_list, i_list, error):
                log.debug('[NamedTree] [SPEC] node %s is the value' %
                          ('/'.join(path)+'/'+ str(k)))
            else:
                log.warning('[NamedTree] [SPEC] unmatched data found')
                for i in i_list:
                    if i not in error[1]:
                        log.warning('[NamedTree] [SPEC] %s of %s is NOT a dict' % ('/' + '/'.join(path)+'/'+k, i.name))
                    else:
                        log.warning('[NamedTree] [SPEC] %s of %s is a dict' % ('/' + '/'.join(path)+'/'+k, i.name))
    return root_node

(OP_KIND_LEAF, OP_KIND_DIR) = list(range(0,2))
def named_tree_travel(op, t_spec, t_list, data, kind = OP_KIND_LEAF):
    ''' A depth first tree travel implmentation with two variants.
    OP_KIND_LEAF means op operate on the leaf node of the tree.
    OP_KIND_DIR means op operate on all the leaves with a common parent.
    '''

    i_list = data['T_list']
    user_data = data['user_data']
    stack = []
    path = []
    error = [CHK_OK, None]

    iter_spec = iter(t_spec)
    root_node = {}
    t_result = root_node

    while True:
        try:
            k = next(iter_spec)
        except StopIteration:
            if len(stack) == 0:
                break
            else:
                si = stack.pop()
                (t_list, t_spec, iter_spec, t_result) = si
                path.pop()
        else:
            if not _check_key(k, t_list, i_list, error):
                for i in error[1]:
                    log.warning('[NamedTree] [Travel] %s has no value at %s' % (i.name, '/'+'/'.join(path)+'/'+str(k)))
            elif isinstance(t_spec[k], dict):
                if _check_dir(k, t_list, i_list, error):
                    si = (t_list, t_spec, iter_spec, t_result)
                    stack.append(si)
                    path.append(str(k))
                    t_list = list(map(lambda d:d[k], t_list))
                    t_spec = t_spec[k]
                    iter_spec = iter(t_spec)
                    t_result[k] = {}
                    t_result = t_result[k]
                else:
                    for i in error[1]:
                        message += '[NamedTree] [Travel] %s of %s is NOT a dict' % ('/'+'/'.join(path)+'/'+str(k), i.name) + '\n'
                    raise TypeError(message)
            else:
                if kind == OP_KIND_LEAF:
                    t_result[k] = op(path, k, t_list, user_data)
                elif kind == OP_KIND_DIR:
                    tmp = op(path, t_spec, t_list, user_data)
                    k = path.pop()
                    si = stack.pop()
                    (t_list, t_spec, iter_spec, t_result) = si
                    t_result[k] = tmp
                else:
                    log.fatal('[NamedTree] [Travel] UNKNOWN kind of operation')
    return root_node

class NamedTree:
    ''' Could be used as a info for a named tree  '''
    #TODO change 'vector' to 'list'
    @classmethod
    def extract_spec(cls, *T_list):
        for T in T_list:
            if T.spec:
                return T.spec
        t_list = list(map(lambda T:T.get_tree(), T_list))
        t_spec = named_tree_get_common(t_list, T_list)
        return t_spec

    def __init__(self, name, tree = None):
        self.name = name
        self.tree = tree
        self.spec = None
        # attributes for print
        self.header_width = None
        self.data_width = None
        self.field_width = None
        self.field_format_spec_start = None
        self.field_format_spec_end = None
        self.field_format_spec = None
        self.field_prefix = None
        self.field_suffix = None

    def get_tree(self):
        return self.tree

    def set_tree(self, tree):
        self.tree = tree

    def set_name(self, name):
        self.name = name

    def _get_branch(self, path):
        '''TODO test'''
        if not self.tree:
            return {}
        node = self.tree
        for name in path:
            node=node[name]
        return node

    def get_branch(self, path):
        '''TODO test'''
        t = self._get_branch(path)
        name = '/'.join(path)
        return NamedTree(name, t)

    def set_branch(self, path, dir_v):
        raise NotImplementedError()

    def get_file(self, path):
        raise NotImplementedError()

    def set_file(self, path, file_v):
        raise NotImplementedError()


# a decorator to implement mathmatic operations
def operator(prefix, kind = OP_KIND_LEAF):
    def real(func):
        def wrapper(*T_list, **user_data):
            data = {'T_list':T_list, 'user_data':user_data}
            t_spec = NamedTree.extract_spec(*T_list)
            t_list = list(map(lambda T:T.get_tree(), T_list))
            r_tree = named_tree_travel(func, t_spec, t_list, data, kind = kind)
            t_names = list(map(lambda T:T.name, T_list))
            R_tree = NamedTree('%s %s' % (prefix, ' '.join(t_names)))
            R_tree.set_tree(r_tree)
            return R_tree
        return wrapper
    return real

class Operator:
    '''The Namespace for Operators of NamedTree
    Some of them have only two operands, so they can be implemented
    as a special math method of NamedTree. Some ones have more than two operands.'''

    @staticmethod
    @operator('the sum of')
    def sum(path, k, t_list, data):
        return sum(map(lambda t: t[k], t_list))

    @staticmethod
    @operator('the substract of')
    def substract(path, k, t_list, data):
        raise NotImplementedError()

    @staticmethod
    @operator('the product of')
    def multiply(path, k, t_list, data):
        raise NotImplementedError()

    @staticmethod
    @operator('the divide of')
    def divide(path, k, t_list, data):
        raise NotImplementedError()

    # average(*vector)
    @staticmethod
    @operator('the average of')
    def average(path, k, t_list, data):
        return sum(map(lambda t: t[k], t_list)) / len(t_list)

    # diff_ratio(T1, T2):
    @staticmethod
    @operator('the diff ratio of')
    def diff_ratio(path, k, t_list, data):
        diff = t_list[1][k] - t_list[0][k]
        ratio = diff / t_list[0][k]
        return ratio

    # union(*vector)
    @staticmethod
    @operator('the union list of')
    def union(path, k, t_list, data):
        return list(map(lambda t: t[k], t_list))

    # scale sum
    @staticmethod
    @operator('the product of')
    def scale_multiply(path, k, t_list, user_data):
        scale = user_data['scale']
        tree = t_list[0]
        return tree[k] * scale

    @staticmethod
    @operator('customized')
    def user_defined(path, k, t_list, user_data):
        v_list = list(map(lambda t: t[k], t_list))
        cb_func = user_data['cb_func']
        if hasattr(user_data, 'cb_data'):
            cb_data = user_data['cb_data']
            return cb_func(cb_data, v_list)
        else:
            return cb_func(v_list)

    @staticmethod
    def branch(path, *vector):
        error = []
        nv = []
        for T in vector:
            try:
                nT = T.get_dir(path)
                nv.append(nT)
            except KeyError as kerror:
                error.append((T, kerror))

        if len(error) != 0:
            raise keyError(error)
        else:
            return nv

NamedTree.Operator = Operator
NamedTree.operator = operator

# a decorator for NamedTreeGroup
# some operations need to be done together to finish one job.
def group_noreturn(kind = OP_KIND_LEAF):
    def real(func):
        def wrapper(group):
            T_list = group.T_list
            data = {'T_list':T_list, 'user_data':group}
            t_spec = NamedTree.extract_spec(*T_list)
            t_list = list(map(lambda T:T.get_tree(), T_list))
            named_tree_travel(func, t_spec, t_list, data, kind = kind)
        return wrapper
    return real

class NamedTreeGroup:
    def __init__(self, *T_list):
        self.T_list = T_list
        self.t_spec = NamedTree.extract_spec(*T_list)
        for T in T_list:
            T.spec = self.t_spec
        self.name = ""

        self.leaf_render = self.__class__.LeafRender(self)
        #TODO path_render

    def __iter__(self):
        return iter(self.T_list)

    def __getattr__(self, name):
        if hasattr(Operator, name):
            op = getattr(Operator, name)
            return lambda **user_data: op(*self.T_list, **user_data)
        else:
            return AttributeError()

    class LeafRender:
        def __init__(self, group):
            self.group = group

            self.path_width = 0
            self.path_width_fixed = 0
            self.path_prefix = ""
            self.path_suffix = ""

            self.data_width = {}
            self.field_width = {}
            #self.field_width_fixed = {}
            self.field_format_spec_start = {}
            self.field_format_spec_end = {}
            self.field_format_spec = {}
            self.field_prefix = {}
            self.field_suffix = {}

            self.header_width = {}

            for T in group:
                n = T.name
                self.data_width[n] = 0
                self.field_width[n] = 0
                #self.field_width_fixed[n] = 0
                self.field_format_spec_start[n] = ""
                self.field_format_spec_end[n] = ""
                self.field_format_spec[n] = ""
                self.field_prefix[n] = ""
                self.field_suffix[n] = ""
                self.header_width[n] = 0

            self.delimiter = "    "
            self.header_template = ""
            self.row_template = ""

        def set_path_width(**width):
            for k in width:
                self.path_width_fixed[k] = width[k]
                
        def set_path_prefix(self, tpl):
            self.path_prefix = prefix

        def set_path_suffix(self, suffix):
            self.path_suffix = suffix
        
        def set_field_format_spec_start(self, **start):
            pass

        def set_field_format_spec_end(self, **end):
            for k in end:
                self.field_format_spec_end[k] = end[k]

        def set_field_suffix(self, **suffix):
            for k in suffix:
                self.field_suffix[k] = suffix[k]

        def merge_field_format_spec(self):
            for T in self.group:
                n = T.name
                if self.data_width[n] == 0:
                    spec = self.field_format_spec_start[n] + self.field_format_spec_end[n]
                else:
                    spec = self.field_format_spec[n] = self.field_format_spec_start[n] + "%d" % self.data_width[n] + self.field_format_spec_end[n]
                self.field_format_spec[n] = spec

        def set_delimiter(self, delimiter):
            self.delimiter = delimiter

        def set_header_width(self, **width):
            for k in width:
                self.header_width[k] = width[k]

        def merge_width(self):
            tmp1 = self.path_width
            tmp2 = self.path_width_fixed
            tmp3 = max(tmp1, tmp2)
            self.path_width = tmp3

            for T in self.group:
                n = T.name
                tmp1 = self.data_width[n]
                tmp1 += len(self.field_prefix[n]) + len(self.field_suffix[n])
                #tmp2 = self.field_width_fixed[T.name]
                #tmp3 = max(tmp1, tmp2)
                self.field_width[n] = tmp1

        def merge_header(self):
            for T in self.group:
                tmp1 = self.field_width[T.name]
                tmp2 = self.header_width[T.name]
                tmp3 = max(tmp1, tmp2)
                self.field_width[T.name] = tmp3
                self.header_width[T.name] = tmp3

        def create_template(self):
            # first column
            tmp_l = list()
            tmp_l_h = list()

            meta_tpl = '%s{%d:%d}%s'
            tpl = meta_tpl % (self.path_prefix,
                              0, #index
                              self.path_width,
                              self.path_suffix)

            tmp_l.append(tpl)
            tmp_l_h.append(tpl)
            # data columns
            i = 1
            for T in self.group:
                n = T.name
                try:
                    if len(self.field_format_spec) > 0:
                        meta_tpl = '%s{%d:%s}%s'
                        tpl = meta_tpl % (
                            self.field_prefix[n],
                            i,
                            self.field_format_spec[n],
                            self.field_suffix[n]
                        )
                    else:
                        meta_tpl = '%s{%d}%s'
                        tpl = meta_tpl % (
                            self.field_prefix[n],
                            i,
                            self.field_suffix[n]
                        )
                    tmp_l.append(tpl)
                    #header
                    meta_tpl = '{%d:%d}'
                    tpl = meta_tpl % (
                        i,
                        self.field_width[n]
                    )
                    tmp_l_h.append(tpl)
                except Exception as error:
                    log.error('tpl for field %d is %s',
                              (i - 1, tpl))
                    log.error('there should be only on %d in field_tpl')
                    raise error
                i += 1

            self.row_template = self.delimiter.join(tmp_l)
            self.header_template = self.delimiter.join(tmp_l_h)
            print('[DEBUG] row_template %s' % self.row_template)
            print('[DEBUG] header_template %s' % self.header_template)
            

    @group_noreturn(kind = OP_KIND_LEAF)
    def _leaf_data_accum_width(path, k, t_list, self):
        leaf_render = self.leaf_render
        l = 0
        for n in path:
            l += len(str(n)) + 1
        l += len(str(k))
        leaf_render.path_width = max(l, leaf_render.path_width)

        leaf_list = list(map(lambda t:t[k], t_list))
        leaf_iter = iter(leaf_list)
        for T in self.T_list:
            n = T.name
            leaf = next(leaf_iter)
            leaf_str = format(leaf, leaf_render.field_format_spec[n])
            leaf_render.data_width[T.name] = max (
                leaf_render.data_width[T.name],
                len(leaf_str)
            )

    @group_noreturn(kind = OP_KIND_LEAF)
    def _leaf_field_print(path, k, t_list, self):
        fields = list(map(lambda t:t[k], t_list))
        first = '/'.join(list(map(lambda d:str(d), path))) + '/' +str(k)
        fields.insert(0, first)
        print(self.leaf_render.row_template.format(*fields))

    def _leaf_header_print(self):
        headers = list(map(lambda T:T.name, self.T_list))
        # place holder for the first column
        headers.insert(0, '')
        # TODO more details is needed
        print(self.leaf_render.header_template.format(*headers))

    def leaf_print(self):
        self.leaf_render.merge_field_format_spec()
        self._leaf_data_accum_width()
        self.leaf_render.merge_width()
        self.leaf_render.merge_header()
        self.leaf_render.merge_field_format_spec()
        self.leaf_render.create_template()
        self._leaf_header_print()
        self._leaf_field_print()
