#!/usr/bin/python

class qaPlan:
    pass

class qaRun:
    pass

class qaCase:
    pass

class qaPack:
    pass

class perfPlan(qaPlan):
    def __init__(self, product, *args, **dargs):
        self.query_range = [0, -1]
        pass

    def get_run(self, build, *args, **dargs):
        pass

class perfRun(qaRun):
    def __init__(self, plan, build, *args, **dargs):
        self.plan = plan
        self.build = build
        self.release = build
        self.arch = arch
        self.host = host

    def get_cases(self, *args, limits = None, **dargs):
        pass


class perfCase(qaCase):
    def __init__(self, name, **dargs):
        pass

class perfPack(qaPack):
    def __init__(self, name, *args, **dargs):
        self.name = name
        self.scripts = list()

    def add_script(self, script):
        self.scripts.append(script)

case2log = {
    'iozone-bigmem-async': (IOzone, DODIOZone, 'iozone-bigmem-async'),
    'iozone-bigmem-fsync': (IOzone, DODIOZone, 'iozone-bigmem-fsync'),
}
