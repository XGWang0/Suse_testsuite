#!/bin/bash
# reference https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server


#
# functions
#

kecho (){
	[[ "${DEBUG}x" == "1x" ]] && builtin echo $@
}

PGROOT=/usr/share/qa/qa_test_pgbench/postgres
PGPATH=${PGROOT}/bin/
PG_CTL_BIN="$PGPATH/pg_ctl"
PG_CREATEDB_BIN="$PGPATH/createdb"
PG_DROPDB_BIN="$PGPATH/dropdb"
PG_INITDB_BIN="$PGPATH/initdb"
PGBENCH_BIN="$PGPATH/pgbench"

export PATH=${PGPATH}:${PATH}
export LD_LIBRARY_PATH=${PGROOT}/lib

if test -d /abuild;then
    PG_DB_ROOT=/abuild/pgdbroot
else
    PG_DB_ROOT=/tmp/pgdbroot
fi
mkdir -p ${PG_DB_ROOT}
kecho "[pg] PG_DB_ROOT is ${PG_DB_ROOT}"

function _exit {
    local _ret=$1
    shift
    kecho "$@"
    exit $_ret
}

# system global
NUMCPUS=`grep processor /proc/cpuinfo | wc -l`
MEMTOTAL_BYTES=`free -b | grep Mem: | awk '{print $2}'`
MACH=$(uname -m)
GROUPID=

function add_postuser {
    if ! id postgres ;then
        groupadd -g 26 -o -r postgres >/dev/null 2>/dev/null \
            && useradd -g postgres -o -r -d /var/lib/pgsql -s /bin/bash \
                       -c "PostgreSQL Server" -u 26 postgres 2>/dev/null
        if test $? -ne 0;then
            _exit 1 "[SYSTEM] Failed to add group and user"
        fi
    fi
	GROUPID=$(grep ^postgres: /etc/group | cut -d: -f3)
}

# Only updates the first occurance of the parameter
update_entry_cnf() {
        PARAMETER=$1
        VALUE=$2
        CONF=$PG_DB_ROOT/postgresql.conf
        LINE=`grep -n "^$PARAMETER" $CONF | cut -d: -f1 | head -1`
        if [ "$LINE" = "" ]; then
                LINE=`grep -n "^#$PARAMETER" $CONF | cut -d: -f1 | head -1`
                if [ "$LINE" = "" ]; then
                        kecho " Failed to locate parameter" $PARAMETER
                fi
        fi
        LINEC=`wc -l $CONF | awk '{print $1}'`
        head -$(($LINE-1)) $CONF > ${CONF}.tmp
        echo $PARAMETER = $VALUE >> ${CONF}.tmp
        tail -$(($LINEC-$LINE)) $CONF >> ${CONF}.tmp

        mv ${CONF}.tmp $CONF
}

# Setup postgresql
function postgresql_init {
    add_postuser
    mkdir -p ${PG_DB_ROOT} && chown postgres:postgres ${PG_DB_ROOT}
    if test $? -ne 0;then
        _exit 1 "[SYSTEM] create dir ${PG_DB_ROOT} failed!"
    else
        kecho "[SYSTEM] created dir ${PG_DB_ROOT}"
    fi

    if test -f ${PG_DB_ROOT}/postmaster.pid;then
        kecho "[pg] stop a service instance"
        service_stop
    fi
    kecho "[SYSTEM] clearing the dir ${PG_DB_ROOT}"
    cd ${PG_DB_ROOT} && rm -rf ./*

    sudo -u postgres ${PG_INITDB_BIN} -D ${PG_DB_ROOT}
    if test $? -ne 0;then
        _exit 1 "[pg] initdb ${PG_DB_ROOT} failed!"
    else
        kecho "[pg] inited the database ${PG_DB_ROOT}"
    fi

    # Update the max connection count if necessary
    update_entry_cnf max_connections $(($NUMCPUS*6))
    # This option just wastes time
    update_entry_cnf update_process_title off
    # Record the PID file
    update_entry_cnf external_pid_file \'$PG_DB_ROOT/postmaster.pid\'
    update_entry_cnf random_page_cost 3.0
    # AutoVacumn
    update_entry_cnf autovacuum on
    # Disable logging
    update_entry_cnf log_connections off
    update_entry_cnf log_duration off
    update_entry_cnf log_hostname off
    # Disable encryption
    update_entry_cnf password_encryption off
    # Use unix domain sockets
    mkdir -p /var/run/postgresql/
    chown postgres /var/run/postgresql/
    chmod a+rwx /var/run/postgresql/
    chmod a+x $HOME
    update_entry_cnf unix_socket_directories \'/var/run/postgresql/\'
    update_entry_cnf unix_socket_group $GROUPID
    update_entry_cnf unix_socket_permissions 0777
}

# global configs for postgresql
PAGESIZE=4096
EFFECTIVE_CACHESIZE=
SHARED_BUFFERS=
WORK_MEM=
function postgresql_configure {
    # Do configuration related to memory
    echo $GROUPID > /proc/sys/vm/hugetlb_shm_group
    # In bytes
    EFFECTIVE_CACHESIZE=$(($MEMTOTAL_BYTES/2))
    SHARED_BUFFERS=$(($MEMTOTAL_BYTES/5))
    case $MACH in
        i686)
            # if your system or PostgreSQL build is 32-bit, it might not be practical to set shared_buffers above 2 ~ 2.5GB.
            #http://rhaas.blogspot.jp/2011/05/sharedbuffers-on-32-bit-systems.html
            i686_2G=$((2*1024*1024*1024))
            test $SHARED_BUFFERS -gt ${i686_2G} &&
                SHARED_BUFFERS=${i686_2G}
            ;;
        *) : ;;
    esac
    #ONLY IO so 32MiB is OK
    WORK_MEM=$((32*1048576))
    TOTALBUFFER_SIZE=$(($EFFECTIVE_CACHESIZE+$WORK_MEM))
	update_entry_cnf work_mem $(($WORK_MEM/1048576))MB
	update_entry_cnf shared_buffers $(($SHARED_BUFFERS/1048576))MB
	update_entry_cnf effective_cache_size $(($EFFECTIVE_CACHESIZE/1048576))MB

	# Do not checkpoint frequently
	# Checkpoints are in 16MB segments so this tuning is to checkpoint
	# when roughly quarter of the shared bufffers have been updated.
	update_entry_cnf checkpoint_segments $((SHARED_BUFFERS/1048576/4))
	update_entry_cnf synchronous_commit on

	# Configure shmem parameters
	echo $TOTALBUFFER_SIZE > /proc/sys/kernel/shmmax
	echo $(($TOTALBUFFER_SIZE*2/$PAGESIZE)) > /proc/sys/kernel/shmall
	ulimit -l $TOTALBUFFER_SIZE
}

function service_start {
    # Do configuration related to memory
    #hugectl?
    sudo -u postgres ${PG_CTL_BIN} -D ${PG_DB_ROOT} start
    # Just wait 10 minutes
    sleep 10
    sudo -u postgres ${PG_CTL_BIN} -D ${PG_DB_ROOT} status
    if test $? -ne 0;then
       _exit 1 "[pg] start service on ${PG_DB_ROOT} failed!"
    else
       kecho "[pg] started the service on ${PG_DB_ROOT}"
    fi
}

function service_stop {
    sudo -u postgres ${PG_CTL_BIN} -D ${PG_DB_ROOT} stop
    sleep 5
    if test $? -ne 0;then
       _exit 1 "[pg] stop service on ${PG_DB_ROOT} failed!"
    else
       kecho "[pg] stop the service on ${PG_DB_ROOT}"
    fi
    rm ${PG_DB_ROOT}/postmaster.pid || true
}

# pgbench

PGHOST=localhost
PGPORT=5432
function pgbench_db_create {
	kecho "[pg] creating the db pgbench"
    su postgres -c "${PG_CREATEDB_BIN} -h $PGHOST -p $PGPORT -U postgres pgbench"
    if test $? -eq 0;then
        kecho "[pg] created the db pgbench"
    else
	    _exit 1 "[pg] create db pgbench failed!"
	fi
}

function pgbench_db_init {
    pgbench_db_create
    SCALE_FACTOR=$((($WORKLOAD_SIZE-30*1048576)/(15*1048576)))
    echo [pg] Initialising db for pgbench: SCALE_FACTOR $SCALE_FACTOR
	/usr/bin/time -f 'QARESULT INIT_DB_LOAD %Uuser %Ssystem %Eelapsed' \
	${PGBENCH_BIN} -q -U postgres -h $PGHOST -p $PGPORT -i -n -s $SCALE_FACTOR pgbench > /dev/null
	if test $? -ne 0;then
	    _exit 1 "[pg] Failed to create the db"
	else
	    kecho "[pg] Succeeded to create the db"
	fi
}

function pgbench_db_fini {
    kecho "[pg] dropping the db pgbench"
    su postgres -c "${PG_DROPDB_BIN} -h $PGHOST -p $PGPORT -U postgres pgbench"
}

function pgbench_db_workload {
	kecho "[pg] starting pgbench"
    #TPC-B (transactions per second)
	/usr/bin/time -f "QARESULT NR_THREADS ${NR_THREADS} WORK_LOAD %Uuser %Ssystem %Eelapsed"  \
	${PGBENCH_BIN} -U postgres -v -h $PGHOST -p $PGPORT -r -l --aggregate-interval=1 -n $READONLY_ARG -c $NR_THREADS \
	-t ${MAX_TRANSACTIONS_PER_CLIENT} pgbench
	if test $? -ne 0;then
	    _exit 1 "[pg] Failed to run"
	else
	     kecho "[pg] Finished one time"
	fi
}

function refresh_profile {
    if test "X${PGBENCH_READONLY}" == XYES; then
        READONLY_ARG="-S" #only select
        MAX_TRANSACTIONS=5000000
    else
        READONLY_ARG=
        MAX_TRANSACTIONS=500000
    fi
    case ${DATABASE_SIZE} in
        medium) WORKLOAD_SIZE=$(($MEMTOTAL_BYTES*3/5))
                ;;
        large) WORKLOAD_SIZE=$(($MEMTOTAL_BYTES*7/5))
               ;;
        xlarge) WORKLOAD_SIZE=$(($MEMTOTAL_BYTES*2))
               ;; #NOT used yet
        small) WORKLOAD_SIZE=$(($SHARED_BUFFERS*4/5))
               if test -z "${READONLY_ARG}";then #RW
                   : MAX_TRANSACTIONS=1000000
               fi
               ;;
        test) WORKLOAD_SIZE=$(($SHARED_BUFFERS/5))
              MAX_TRANSACTIONS=10
               ;;
        *) _exit 1 "NOT be reached here";;
    esac
    kecho "ARG MAX_TRANSACTIONS ${MAX_TRANSACTIONS}"
    kecho "ARG READONLY_ARG ${READONLY_ARG}"
    kecho "ARG DATABASE_SIZE ${DATABASE_SIZE}"
    THREADS=
    START_THREAD=1
    END_THREAD=$(($NUMCPUS*4))
    if [ $END_THREAD -ge 32 ]; then
	    THREADS=`seq $START_THREAD 4 8`
	    THREADS="$THREADS `seq 12 9 32`"
	    THREADS="$THREADS `seq 48 31 $END_THREAD`"
    elif [ $END_THREAD -ge 8 ]; then
	    THREADS=`seq $START_THREAD 3 8`
	    THREADS="$THREADS `seq 12 6 $END_THREAD`"
    else
	    THREADS=`seq $START_THREAD 2 $END_THREAD`
    fi
    if [ `echo $THREADS | awk '{print $NF}'` -ne $END_THREAD ]; then
	    THREADS="$THREADS $END_THREAD"
    fi
    kecho -n ARG THREADS 
    for num in $THREADS; do
        kecho -n " $num"
    done
    echo
    CACHE_HOT=YES
    kecho "ARG CACHE_HOT ${CACHE_HOT}"
}

function pgbench_run {
    # su postgres /usr/bin/psql -c 'createdb pgbench;'
    # createdb -U postgres pgbench
    for NR_THREADS in $THREADS; do
        # Start the database
        MAX_TRANSACTIONS_PER_CLIENT=$(($MAX_TRANSACTIONS / $NR_THREADS))
        service_start
        pgbench_db_init

	    if [ "$CACHE_HOT" != "YES" ]; then
		    kecho "Discarding database cache for cold startup"
		    service_stop
		    echo 3 > /proc/sys/vm/drop_caches
		    service_start
 	    fi

        pgbench_db_workload
        pgbench_db_fini
        service_stop
    done
}

function usage() {
        echo "
Usage:   $0 [-h] [-r] [-t target work sizez] [-s scale factor]

Options:
         -r   Read only or not
         -h   Print this help text and exit successfully
         -s   report this scale factor in output
"
        exit 1
}

# main function
DATABASE_SIZE=small
PGBENCH_READONLY=
while getopts "hrs:tD" optchar; do
    case "$optchar" in
        r)      PGBENCH_READONLY=YES ;;
        s)      DATABASE_SIZE="$OPTARG" ;;
        t)      DATABASE_SIZE="test" ;;
        D)      DEBUG="1" ;;
        *)      usage ;;
    esac
done
shift $((OPTIND - 1))

if [ "${DEBUG}x" == "1x" ]; then
	echo "[testing run in DEBUG mode]"
	postgresql_init 
	postgresql_configure 
	refresh_profile 
	pgbench_run 
else
	echo "[testing run in quite mode]"
	postgresql_init 2>&1 >/dev/null
	postgresql_configure 2>&1 >/dev/null
	refresh_profile 2>&1 >/dev/null
	pgbench_run 
fi
