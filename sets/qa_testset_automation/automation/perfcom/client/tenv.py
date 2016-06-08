#!/usr/bin/python3

import itertools
import configparser
from .error import *
from . import apicall

class OSDistro:
    def __init__(self, arch, release, build, kernel):
        self.arch = arch
        self.release = release
        self.build = build
        self.kernel = kernel

    def __str__(self):
        return "{arch} {release} {build} {kernel}".format(**self.__dict__)

class OSComponent:
    def __init__(self, category, category_value = None):
        self.category = category
        if self.has_category_value():
            self.category_value = category_value
        else:
            self.category_value = None

    def has_category_value(self):
        return self.category in ("io",)

class OSInst:
    def __init__(self, swap_size, rootfs_type, rootfs_size):
        self.swap_size = swap_size
        self.rootfs_type = rootfs_type
        self.rootfs_size = rootfs_size

class Machine:
    def __init__(self, host):
        self.host = host
    def __str__(self):
        return "{}".format(self.host)

class Tenv:
    def __init__(self, distro, component, inst, machine, extra = None):
        self.distro = distro
        self.component = component
        self.inst = inst
        self.machine = machine
        self.extra = extra
        self._id = None

    def _p_q_args(self):
        pargs = {}
        pargs["arch"] = self.distro.arch
        pargs["release"] = self.distro.release
        pargs["build"] = self.distro.build
        pargs["kernel"] = self.distro.kernel
        pargs["host"] = self.machine.host
        pargs["category"] = self.component.category
        qargs = {}
        if self.component.has_category_value():
            qargs["category_value"] = self.component.category_value
        qargs["swap_size"] = self.inst.swap_size
        qargs["rootfs_type"] = self.inst.rootfs_type
        qargs["rootfs_size"] = self.inst.rootfs_size
        if self.extra:
            qargs["extra"] = self.extra
        return pargs, qargs

    def get_id(self, dynapi):
        if self._id: return self._id
        pargs, qargs = self._p_q_args()
        ret = dynapi.get("/api/report/v1/env", pargs, qargs).json()
        self._id = ret["id"]
        return self._id

    def new_id(self, dynapi):
        if self._id: return self._id
        pargs, qargs = self._p_q_args()
        ret = dynapi.post("/api/report/v1/env", pargs, qargs, None).json()
        self._id = ret["id"]
        return self._id

class TenvPlain:
    DEFAULT_SWAP_SIZE = "32763"
    DEFAULT_ROOFS_TYPE = "btrfs"
    DEFAULT_ROOFS_SIZE = "51200"
    def __init__(self, stream, name="", no_category=False):
        self.stream = stream
        self.name = name
        self.no_category = no_category
        self.parse()

    def parse(self):
        cf = configparser.ConfigParser()
        cf.read_file(itertools.chain(("[global]",), self.stream))
        try:
            section = cf["global"]
            arch = section["_QASET_ARCH"]
            release = section["_QASET_RELEASE"]
            build = section["_QASET_BUILD"]
            kernel = section["_QASET_KERNEL"]
            host = section["_QASET_HOSTNAME"]
            swap_size = section.get("_QASET_SWAP_SIZE", self.DEFAULT_SWAP_SIZE)
            rootfs_type = section.get("_QASET_ROOTFS_TYPE", self.DEFAULT_ROOFS_TYPE)
            rootfs_size = section.get("_QASET_ROOTFS_SIZE", self.DEFAULT_ROOFS_SIZE)
        except KeyError as e:
            raise InvalidLogError("Fail to parse {0}: No Key {1}".format(self.name, e.args[0]))
        else:
            self.distro = OSDistro(arch, release, build, kernel)
            self.machine = Machine(host)
            #TODO this is a trade off. It will be remove in future.
            swap_size = self.DEFAULT_SWAP_SIZE
            rootfs_size = self.DEFAULT_ROOFS_SIZE
            self.inst = OSInst(swap_size, rootfs_type, rootfs_size)
        try:
            category = section["_QASET_CATEGORY_TYPE"]
            category_value = section["_QASET_CATEGORY_VALUE"]
        except KeyError as e:
            if not self.no_category :
                raise InvalidLogError("Fail to parse {}".format(self.name)) from e
        else:
            if category == "FS": category = "io"
            self._component = OSComponent(category, category_value)

    @property
    def component(self):
        if self.no_category:
            raise InvalidLogError("No category to parser")
        return self._component
