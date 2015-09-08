import dod
import sys

class Error(Exception):
    pass

class DODRender:
    def __init__(self, DOD_list, name = "NoName"):
        self.DOD_list = DOD_list
        self.name = name
        self.dod_names = list()

    def print_table(self):
        raise NotImplementedError()

    def print_header(self):
        raise NotImplementedError()

    def print_footer(self):
        raise NotImplementedError()

    def print_description(self):
        raise NotImplementedError()

class DODRenderCLComparsion(DODRender):
    def __init__(self, dod_list, dod_comparsion_list, name = "NoName"):
        '''
        first dod is the base 
        '''
        self.dod_list = dod_list
        self.dod_comparsion_list = dod_comparsion_list
        self.name = name
        self.dod_names = list()

    def get_list(self):
        self.out_list = list()
        self.out_list.append(self.dod_list[0])
        dod_iter = iter(self.dod_list[1:])
        dod_comparsion_iter = iter(self.dod_comparsion_list)
        while True:
            try:
                self.out_list.append(next(dod_iter))
            except StopIteration:
                break
            try:
                self.out_list.append(next(dod_comparsion_iter))
            except StopIteration:
                self.out_list.pop()
                logging.warning("[dodrender] number comparsion results unmatched")
                break

    def _travel(self, func):
        def _wrapper(path, leaf_list, self):
            func(path, leaf_list)
        dod.dod_vector_travel_depth(self.out_list, _wrapper, self)
        
    def _print_record(self, path, vector):
        stat_key_list = list()
        stat_dict_list = list()
        ref0 = vector[0]
        c1 = list()
        c_ref0 = list()
        stat_dict = dict()
        for k in ref0:
            stat_key_list.append(k)
            stat_dict[k]=str(ref0[k])
        stat_dict_list.append(stat_dict)

        c_iter = iter(vector[1:])
        while True:
            try:
                dict_1 = next(c_iter)
                dict_2 = next(c_iter)
            except StopIteration:
                break
            stat_dict_1 = dict()
            stat_dict_2 = dict()
            for k in ref0:
                stat_dict_1[k] = str(dict_1[k])
                stat_dict_2[k] = "{0:2.2f}".format(dict_2[k])
            stat_dict_list.append(stat_dict_1)
            stat_dict_list.append(stat_dict_2)

        return (str(path), stat_key_list, stat_dict_list)

    def init_width(self):
        self.width = list()
        self.width.append(0)
        for i in self.out_list:
            self.width.append(0)

    def _cal_width(self, path, leaf_list):
        path_str, stat_key_list, stat_dict_list = self._print_record(path, leaf_list)

        for stat_key in stat_key_list:
            c0 = "%s/%s" % (path_str, stat_key)
            self.width[0] = max(self.width[0], len(c0))

        i = 1
        stat_dict_iter = iter(stat_dict_list)
        while i < len(self.width):
            stat_dict = next(stat_dict_iter)
            for stat_key in stat_key_list:
                self.width[i] = max(self.width[i], len(stat_dict[stat_key]))
            i += 1

    def cal_width(self):
        self._travel(self._cal_width)

    def after_cal_width(self):
        i = 1
        fmt = '{0:%ds}' % self.width[0]
        while i < len(self.width):
            fmt = fmt + '\t{%d:%ds}' % (i, self.width[i])
            i += 1
        self.line_fmt = fmt

    def print_record(self, path, leaf_list):
        path_str, stat_key_list, stat_dict_list = self._print_record(path, leaf_list)
        for stat_key in stat_key_list:
            left_part = list()
            for stat_dict in stat_dict_list:
                left_part.append(stat_dict[stat_key])
            print(self.line_fmt.format("%s/%s" % (path_str, stat_key), *left_part))
        
    def print_table(self):
        self._travel(self.print_record)

    def print_header(self):
        pass

    def print_footer(self):
        pass

    def print_description(self):
        print("Statitcs for %s" % self.name)

    def render(self):
        self.get_list()
        self.print_description()
        print()
        self.init_width()
        self.cal_width()
        self.after_cal_width()
        self.print_header()
        print()
        self.print_table()
        print()
        self.print_footer()


class DODRenderHTML(DODRender):
    pass
