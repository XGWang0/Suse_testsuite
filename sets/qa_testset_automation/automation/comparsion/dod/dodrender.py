import dod
import sys

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

class DODRenderCLSimple(DODRender):
    def _travel(self, func):
        def _wrapper(path, leaf_list, self):
            func(path, leaf_list)
        dod.dod_vector_travel_depth(list(map(lambda D:D.dod, self.DOD_list)), _wrapper, self)
        
    def _print_line(self, path, leaf_list):
        line = list()
        line.append(str(path))
        for leaf in leaf_list:
            line.append(str(leaf))
        return line

    def init_width(self):
        self.width = list()
        self.width.append(0)
        for i in self.DOD_list:
            self.width.append(0)
        dod_names = iter(self.dod_names)
        i = 1
        while i < len(self.dod_names):
            n = next(dod_names)
            self.width[i] = max(self.width[i], len(n))
            i += 1

    def cal_width(self, path, leaf_list):
        i = 0
        line = self._print_line(path, leaf_list)
        field = iter(line)
        while i < len(self.width):
            f = next(field)
            self.width[i] = max(self.width[i], len(f))
            i += 1

    def after_cal_width(self):
        i = 1
        fmt = '{0:%ds}' % self.width[0]
        while i < len(self.width):
            fmt = fmt + '\t{%d:%ds}' % (i, self.width[i])
            i += 1
        self.line_fmt = fmt

    def print_line(self, path, leaf_list):
        line = self._print_line(path, leaf_list)
        print(self.line_fmt.format(*line))

    def print_table(self):
        self._travel(self.print_line)

    def print_header(self):
        pass

    def print_footer(self):
        pass

    def print_description(self):
        print("Statitcs for %s" % self.name)

    def render(self):
        self.print_description()
        print()
        self.init_width()
        self._travel(self.cal_width)
        self.after_cal_width()
        self.print_header()
        print()
        self.print_table()
        print()
        self.print_footer()

class DODRenderHTML(DODRender):
    pass
