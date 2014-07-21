#!/bin/bash

function _exit {
    local _ret=$1
    shift
    echo "$@"
    exit $_ret
}

function service_stop {
    sudo -u postgres -g postgres pg_ctl stop -D ${PG_DB_ROOT}
}

if test -d /abuild;then
    PG_DB_ROOT=/abuild/pgdb
else
    PG_DB_ROOT=/tmp/pgdb
fi


sudo -u postgres -g postgres mkdir -p ${PG_DB_ROOT}
if test $? -ne 0;then
    _exit 1 "[SYSTEM] create dir ${PG_DB_ROOT} failed!"
else
    echo "[SYSTEM] created dir ${PG_DB_ROOT}"
fi

if test -f ${PG_DB_ROOT}/postmaster.pid;then
    echo "[pg] stop a service instance"
    service_stop
fi

echo "[SYSTEM] clearing the dir ${PG_DB_ROOT}"
cd ${PG_DB_ROOT} && rm -rf ./*

sudo -u postgres -g postgres initdb -D ${PG_DB_ROOT}
if test $? -ne 0;then
    _exit 1 "[pg] initdb ${PG_DB_ROOT} failed!"
else
    echo "[pg] created the database ${PG_DB_ROOT}"
fi

sudo -u postgres -g postgres pg_ctl start -D ${PG_DB_ROOT}
if test $? -ne 0;then
    _exit 1 "[pg] start service on ${PG_DB_ROOT} failed!"
else
    echo "[pg] started the service on ${PG_DB_ROOT}"
fi

echo "[pg] creating the db pgbench"
for i in seq 10;do
    sleep 5 #wait for the service finishes
    createdb -U postgres pgbench
    if test $? -eq 0;then
        PG_DB_CREATED=YES
        break
    fi
done

if test -z ${PG_DB_CREATED};then
    service_stop
    _exit 1 "[pg] create db pgbench failed!"
else
    echo "[pg] created the db pgbench"
fi

echo "[pg] starting TEST LOAD"
/usr/bin/time -f 'STAT_LOAD %Uuser %Ssystem %Eelapsed' pgbench -U postgres -i -s 4080 pgbench

echo "[pg] starting TEST SELECT"
/usr/bin/time -f 'STAT_SELECT %Uuser %Ssystem %Eelapsed' pgbench -c 7 -t 100000 pgbench

echo "[pg] starting TEST SELECT 2"
/usr/bin/time -f 'STAT_SELECT_S %Uuser %Ssystem %Eelapsed' pgbench -S -c 7 -t 100000 pgbench

service_stop
