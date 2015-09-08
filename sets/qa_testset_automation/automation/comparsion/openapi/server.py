#!/usr/bin/python

from bottle import route, run, template, request
import json
import os
import logging

import logDB
perfdb = logDB.get_perfdb()

import parserManager

class Error(Exception):
    pass

@route('/api/hello')
def hello(**dargs):
    rdict = dict()
    for k in request.query:
        rdict[k] = request.query[k]
    return json.dumps({'Return': True, 'Args':rdict})

@route('/api/try/type')
def hello(**dargs):
    rdict = dict()
    tdict = dict()
    for k in request.query:
        #TODO UTF-8 q=%E4%B8%AD%E6%96%87
        print("request.query[%s] %s" % (k, request.query[k]))
        rdict[k] = request.query[k]
        tdict[k] = str(type(rdict[k]))
    return json.dumps({'Return': True, 'Args':rdict, 'Type':tdict})

@route('/api/log/perf/get_log')
def api_log_perf_get_log(**kwargs):
    required_fields = ('release', 'build', 'arch')
    for k in required_fields:
        if not k in request.query:
            return json.dumps({'Return': False, 'Error': "Args Missing %s" % k})
    q = request.query
    try:
        records = perfdb.get_log_by_build(q['release'], q['build'], q['arch']):
    except Exception as e:
        #TODO return error within http status
        raise(e)
    return json.dumps(records)

@route('/api/log/perf/get_statistics')
def api_log_perf_get_statistics(**kwargs):
    required_fields = ('release', 'build', 'arch', 'host', 'suite') 
    for k in required_fields:
        if not k in request.query:
            return json.dumps({'Return': False, 'Error': "Args Missing %s" % k})
    q = request.query
    dod = app.log_perf_get_statistic(q['release'], q['build'], q['arch'],
                                         q['host'], q['suite'], q['case'])
    return json.dumps(dod)

@route('/api/log/perf/get_statistics_comparsion')
def log_perf_get_statistic_comparsion(**kwargs):
    required_fields = ('release1', 'build1', 'arch', 'host', 'suite',
                       'release2', 'build2')
    q = dict()
    try:
        q['arch'] = request.query['arch']
        q['host'] = request.query['host']
        q['suite'] = request.query['suite']
        q['release1'] = request.query['release1']
        q['build1'] = request.query['build1']
        q['release2'] = request.query['release2']
        q['build2'] = request.query['build2']
    except KeyError:
        return json.dumps({'Return': False, 'Error': "Args Missing %s" % k})

    rdod = app.log_perf_get_statistic_comparsion(**q)
    return json.dumps(rdod)

run(host='', port=8080, debug=True)
