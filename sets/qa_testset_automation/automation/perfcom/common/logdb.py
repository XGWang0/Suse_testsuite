#!/usr/bin/python3


def query_log(dynapi, distro, machine, run_id, suite):
    pargs = {}
    pargs["arch"] = distro.arch
    pargs["release"] = distro.release
    pargs["build"] = distro.build
    pargs["kernel"] = distro.kernel
    pargs["run_id"] = run_id
    pargs["host"] = machine.host
    qargs = {}
    qargs["suite"] = suite
    logs = dynapi.get("/api/log/v1/host", pargs, qargs).json()["logs"]
    return logs


def query_cases(dynapi, distro, machine, run_id):
    pargs = {}
    pargs["arch"] = distro.arch
    pargs["release"] = distro.release
    pargs["build"] = distro.build
    pargs["kernel"] = distro.kernel
    pargs["run_id"] = run_id
    pargs["host"] = machine.host
    cases = dynapi.get("/api/log/v1/case", pargs, {}).json()["cases"]
    return cases
