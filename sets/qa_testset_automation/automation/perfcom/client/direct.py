#!/usr/bin/python3
import json

def reportdb(dynapi, SQLs):
    endpoint = "/api/report/hidden/proxy/reportdb"
    return direct_sql(dynapi, endpoint, SQLs)

def qadb(dynapi, SQLs):
    endpoint = "/api/report/hidden/proxy/qadb"
    return direct_sql(dynapi, endpoint, SQLs)

def direct_sql(dynapi, endpoint, SQLs):
    return dynapi.post(endpoint, {}, {}, {"SQLs":SQLs}).json()
