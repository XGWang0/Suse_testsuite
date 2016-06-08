#!/usr/bin/python3

import http.client
import urllib.parse
import re
import json
from .error import *
from .debug import *

#
# arg spec
# @n: name of the arg
# @t: type of the arg
# @o: if the arg is optional. Default False
# all args in pargs should not be optional.
#
API_GET = {
    "/api/report/v1/comparison/run":{
        "pargs":[
            {"n":"suite"},
            {"n":"case"},
            {"n":"q_tenv_id"},
            {"n":"r_tenv_id"},
            {"n":"q_run_id"},
            {"n":"r_run_id"}
        ],
        "qargs":[]
    },
    "/api/report/v1/comparison/plan/html":{
        "pargs":[
            {"n":"suite"},
            {"n":"case"},
            {"n":"q_tenv_id"},
            {"n":"r_tenv_id"}
        ]
    },
    "/api/report/v1/comparison/plan/id":{
        "pargs":[
            {"n":"suite"},
            {"n":"case"},
            {"n":"q_tenv_id"},
            {"n":"r_tenv_id"}
        ]
    },
    "/api/report/v1/env":{
        "pargs":[
            {"n":"arch"},
            {"n":"release"},
            {"n":"build"},
            {"n":"kernel"},
            {"n":"host"},
            {"n":"category"}
        ],
        "qargs":[
            {"n":"category_value", "o":True},
            {"n":"swap_size"},
            {"n":"rootfs_type"},
            {"n":"rootfs_size"},
            {"n":"extra", "o":True}
        ]
    },
    "/api/report/v1/plan/distropair/references_incomplete":{
        "pargs":[
            {"n":"arch"},
            {"n":"release"},
            {"n":"build"}
        ]
    },
    "/api/report/v1/plan/distropair/run-id":{
        "pargs":[
            {"n":"arch"},
            {"n":"release"},
            {"n":"build"},
            {"n":"kernel"}
        ]
    },
    "/api/log/v1/host":{
        "pargs":[
            {"n":"arch"},
            {"n":"release"},
            {"n":"build"},
            {"n":"kernel"},
            {"n":"run_id"},
            {"n":"host"}
        ],
        "qargs":[
            {"n":"suite"},
            {"n":"case", "o":True}
        ]
    },
    "/api/log/v1/case":{
        "pargs":[
            {"n":"arch"},
            {"n":"release"},
            {"n":"build"},
            {"n":"kernel"},
            {"n":"run_id"},
            {"n":"host"}
        ]
    }
}
API_POST = {
    "/api/report/v1/env":{
        "pargs":[
            {"n":"arch"},
            {"n":"release"},
            {"n":"build"},
            {"n":"kernel"},
            {"n":"host"},
            {"n":"category"}
        ],
        "qargs":[
            {"n":"category_value", "o":True},
            {"n":"swap_size"},
            {"n":"rootfs_type"},
            {"n":"rootfs_size"},
            {"n":"extra", "o":True},
        ]
    },
    "/api/report/v1/status/run":{
        "pargs":[
            {"n":"suite"},
            {"n":"case"},
            {"n":"q_tenv_id"},
            {"n":"r_tenv_id"},
            {"n":"q_run_id"},
            {"n":"r_run_id"},
            {"n":"status"}
        ],
        "qargs":[]
    },
    "/api/report/v1/plan/distropair":{
        "pargs":[
            {"n":"arch"}
        ],
        "qargs":[]
        #jargs
    },
    "/api/report/hidden/proxy/reportdb":{
        "pargs":[],
        "qargs":[],
        #"jargs":{"n":"SQLs"}
    },
    "/api/report/hidden/proxy/qadb":{
        "pargs":[],
        "qargs":[],
        #"jargs":{"n":"SQLs"}
    }
}

class dynLinkFunc:
    multiton = {}
    def __new__(cls, endpoint, *noused):
        if not endpoint in cls.multiton:
            self = super().__new__(cls)
            cls.multiton[endpoint] = self
            self._initialized = False
        return cls.multiton[endpoint]

    def __init__(self, endpoint, method = "GET"):
        if self._initialized: return
        self.method = method
        self.endpoint = endpoint
        self._init_api(endpoint)
        self._initialized = True

    def _init_api(self, endpoint):
        if self.method == "GET":
            try:
                self.api = API_GET[endpoint]
            except KeyError as e:
                raise ProgrammingError(str(e))
        elif self.method == "POST":
            try:
                self.api = API_POST[endpoint]
            except KeyError as e:
                raise ProgrammingError(str(e))
        else:
            raise ProgrammingError("{} not supported")

    def p2str(self, params):
        '''params is a dict
        a string like "param01/param01 ... /paramXX"
        is return
        '''
        vl = []
        try:
            for parg in self.api["pargs"]:
                quoted = urllib.parse.quote(str(params[parg["n"]]))
                vl.append(quoted)
        except KeyError as e:
            raise ArgError(str(e))
        return "/".join(vl)

    def q2str(self, params):
        '''params is a dict
        a string like "name01=value01&name02=value02 ... &nameXX=value-XX"
        is return
        '''
        vl = []
        for qarg in self.api["qargs"]:
            name = qarg["n"]
            try:
                optional = qarg["o"]
            except KeyError:
                optional = False
            if name in params:
                quoted = urllib.parse.quote(str(params[name]))
                vl.append("{0}={1}".format(name, quoted))
            elif not optional:
                raise ArgError("miss {}".format(name))
        return "&".join(vl)

    def _has_query(self):
        return "qargs" in self.api and self.api["qargs"]

    def get_url(self, pparams, qparams):
        url = self.endpoint
        if self.api["pargs"]:
            url = "{0}/{1}".format(url, self.p2str(pparams))
        if self._has_query():
            query_part = self.q2str(qparams)
            if query_part:
                url = "{0}?{1}".format(url, query_part)
        return url

    def get_body(self, body):
        #TODO json
        return body

class apiReturn:
    def __init__(self, content):
        self.content = content

    def json(self):
        try:
            content = json.loads(self.content.decode('utf-8'))
        except (ValueError, TypeError, UnicodeDecodeError) as e:
            raise e
        devlog_obj(content)
        return content["data"]

    def plain(self):
        return self.content

    def utf8(self):
        return self.content.decode

class apiClient:
    def __init__(self, site, port):
        self.site = site
        self.port = port
        self.con = http.client.HTTPConnection(self.site, self.port)

    def http_get(self, url):
        devlogR("api_get: {0}".format(url))
        self.con.request('GET', url)
        rsp = self.con.getresponse()
        if rsp.status == 200:
            content = rsp.read()
            return apiReturn(content)
        elif rsp.status == 404:
            content = rsp.read()
            content_type = rsp.getheader("Content-Type", "")
            if re.match(".*json.*", content_type):
                content = json.loads(content.decode("utf-8"))
            raise HTTPError(rsp.status, content)
        else:
            raise HTTPError(rsp.status)

    def http_post(self, url, body):
        devlogR("api_post: {0}".format(url))
        #TODO body type
        body = json.dumps(body)
        headers = {}
        headers['CONTENT-TYPE'] = 'application/vnd.api+json'
        self.con.request('POST', url, body, headers)
        rsp = self.con.getresponse()
        if rsp.status == 200:
            content = rsp.read()
            return apiReturn(content)
        elif rsp.status == 404:
            content = rsp.read()
            content_type = rsp.getheader("Content-Type", "")
            if re.match(".*json.*", content_type):
                content = json.loads(content.decode("utf-8"))
            raise HTTPError(rsp.status, content)
        else:
            raise HTTPError(rsp.status)

    @staticmethod
    def _quote_args(args):
        nargs = {}
        for k,v in args.items():
            nargs[k] = urllib.parse.quote(str(v))

    def call(self, dynLink, pargs = {}, qargs = {}, body = None):
        url = dynLink.get_url(pargs, qargs)
        if dynLink.method == "GET":
            return self.http_get(url)
        elif dynLink.method == "POST":
            body = dynLink.get_body(body)
            return self.http_post(url, body)
        else:
            raise ErrorNotSupport(dynLink.method)

class dynAPI:
    def __init__(self, client):
        self.client = client

    def get(self, endpoint, pargs, qargs):
        return self.client.call(dynLinkFunc(endpoint, "GET"), pargs, qargs, None)

    def post(self, endpoint, pargs, qargs, body):
        return self.client.call(dynLinkFunc(endpoint, "POST"), pargs, qargs, body)

