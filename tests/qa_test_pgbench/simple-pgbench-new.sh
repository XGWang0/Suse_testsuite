#!/bin/bash

READONLY=
PGPATH=/usr/share/qa/qa_test_pgbench/postgres/bin/
while getopts hr:t:s: optchar ; do

    case "$optchar" in

      h)      usage
              exit 0                                 ;;
      r)      READONLY=$OPTARG                       ;;
      s)      SCALE_FACTOR="$OPTARG"                 ;;
      *)      usage
              exit "$exitcode" ;;
    esac
done
shift $((OPTIND - 1))

function usage() {
        echo "
Usage:   $0 [-h] [-r readonly] [-t target work sizez] [-s scale factor]

Options:
         -r   Read only or not
         -h   Print this help text and exit successfully
         -s   report this scale factor in output
"    
        return 0
}


NUMCPUS=`grep processor /proc/cpuinfo | wc -l`
MEMTOTAL_BYTES=`free -b | grep Mem: | awk '{print $2}'`

if test -d /abuild;then
    PG_DB_ROOT=/abuild/pgdbsmall
else
    PG_DB_ROOT=/tmp/pgdbsmall
fi

#install-depends bison gcc-c++ libstdc++-devel popt-devel zlib-devel

# Only updates the first occurance of the parameter
update_entry_cnf() {
        PARAMETER=$1
        VALUE=$2
        CONF=$PG_DB_ROOT/postgresql.conf

        LINE=`grep -n "^$PARAMETER" $CONF | cut -d: -f1 | head -1`
        if [ "$LINE" = "" ]; then
                LINE=`grep -n "^#$PARAMETER" $CONF | cut -d: -f1 | head -1`
                if [ "$LINE" = "" ]; then
                        echo " Failed to locate parameter" $PARAMETER
                fi
        fi
        LINEC=`wc -l $CONF | awk '{print $1}'`
        head -$(($LINE-1)) $CONF > ${CONF}.tmp
        echo $PARAMETER = $VALUE >> ${CONF}.tmp
        tail -$(($LINEC-$LINE)) $CONF >> ${CONF}.tmp

        mv ${CONF}.tmp $CONF
}

function _exit {
    local _ret=$1
    shift
    echo "$@"
    exit $_ret
}

function service_stop {
    sudo -u postgres -g postgres $PGPATH/pg_ctl stop -D ${PG_DB_ROOT}
    if test $? -ne 0;then
       _exit 1 "[pg] stop service on ${PG_DB_ROOT} failed!"
    else
       echo "[pg] stop the service on ${PG_DB_ROOT}"
    fi

}

function service_start {
    # Start the database
    sudo -u postgres -g postgres $PGPATH/pg_ctl start -D ${PG_DB_ROOT}
    if test $? -ne 0;then
       _exit 1 "[pg] start service on ${PG_DB_ROOT} failed!"
    else
       echo "[pg] started the service on ${PG_DB_ROOT}"
    fi
}

mkdir -p ${PG_DB_ROOT} && chown postgres:postgres ${PG_DB_ROOT}
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

#Init database
sudo -u postgres -g postgres $PGPATH/initdb -D ${PG_DB_ROOT}
if test $? -ne 0;then
    _exit 1 "[pg] initdb ${PG_DB_ROOT} failed!"
else
    echo "[pg] inited the database ${PG_DB_ROOT}"
fi

# Update the max connection count if necessary
echo o Setting max_connections: $(($NUMCPUS*6))
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

echo "set parameters of postgres successfully"

#run test
EFFECTIVE_CACHESIZE=$((756*1048576))
SHARED_BUFFERS=$((32*1048576))
WORK_MEM=$((32*1048576))
MAX_TIME=
MAX_TRANSACTIONS=auto
SCALE_FACTOR=1
VACUUM_ARG=-n
CACHE_HOT=no
READONLY_ARG=
READONLY=
PGHOST=localhost
PGPORT=5432
CACHE_HOT=yes

# pgbench
OLTP_CACHESIZE=$(($MEMTOTAL_BYTES/2))
OLTP_SHAREDBUFFERS=$((MEMTOTAL_BYTES/5))
OLTP_PAGESIZES="default"
MAX_THREADS=$((NUMCPUS*4))
TOTALBUFFER_SIZE=$(($EFFECTIVE_CACHESIZE+$WORK_MEM))

if [ "$OLTP_CACHESIZE" != "" ]; then
   EFFECTIVE_CACHESIZE=$OLTP_CACHESIZE
fi

if [ "$OLTP_SHAREDBUFFERS" != "" ]; then
   SHARED_BUFFERS=$OLTP_SHAREDBUFFERS
fi

if [ "$DATABASE_SIZE" = "small" ]; then
       TARGET_WORKLOAD_SIZE=$((OLTP_SHAREDBUFFERS*4/5))
elif [ "$DATABASE_SIZE" = "medium" ]; then
         TARGET_WORKLOAD_SIZE=$((MEMTOTAL_BYTES*3/5))
elif  [ "$DATABASE_SIZE" = "large" ]; then
         TARGET_WORKLOAD_SIZE=$((MEMTOTAL_BYTES*7/5))
else
        TARGET_WORKLOAD_SIZE=$((OLTP_SHAREDBUFFERS*4/5))
fi

PGBENCH_SCALE_FACTOR=$(((TARGET_WORKLOAD_SIZE-30*1048576)/(15*1048576)))

update_entry_cnf work_mem $(($WORK_MEM/1048576))MB
update_entry_cnf shared_buffers $((SHARED_BUFFERS/1048576))MB
update_entry_cnf effective_cache_size $(($EFFECTIVE_CACHESIZE/1048576))MB

# Do not checkpoint frequently
# Checkpoints are in 16MB segments so this tuning is to checkpoint
# when roughly quarter of the shared bufffers have been updated.
update_entry_cnf checkpoint_segments $((SHARED_BUFFERS/1048576/4))
update_entry_cnf synchronous_commit on

if [ "$PAGESIZE"="default" ] ; then
        PAGESIZE=4096
fi


# Configure shmem parameters
echo $TOTALBUFFER_SIZE > /proc/sys/kernel/shmmax
echo $(($TOTALBUFFER_SIZE*2/$PAGESIZE)) > /proc/sys/kernel/shmall
ulimit -l $TOTALBUFFER_SIZE

if [ "$READONLY" = "yes" ]; then
        READONLY_ARG=-S
fi

if [ "$MAX_TRANSACTIONS" = "auto" ]; then
	FLOOR=15000
        WORKLOAD_SIZE=$((SCALE_FACTOR*15*1048576+30*1048576))
#        MAX_TRANSACTIONS=`awk "{ if (\\$1 >= \$WORKLOAD_SIZE) print \\$2 }" /tmp/coordinates | head -1`
        MAX_TRANSACTIONS=100 
	if [ "$MAX_TRANSACTIONS" = "" ]; then
                MAX_TRANSACTIONS=$FLOOR
        fi
        if [ $MAX_TRANSACTIONS -lt $FLOOR ]; then
                MAX_TRANSACTIONS=$FLOOR
        fi
fi


THREADS=
START_THREAD=1
END_THREAD=$MAX_THREADS
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

chown -R postgres:postgres ${PG_DB_ROOT}

# su postgres /usr/bin/psql -c 'createdb pgbench;'
#createdb -U postgres pgbench
for NR_THREADS in $THREADS; do
        # Start the database
        service_start
        sleep 20

	echo "[pg] creating the db pgbench"
        #su postgres $PSQL -c 'createdb pgbench;'
        #su postgres $PSQL "template1 -c 'createdb  pgbench;'"
        su postgres -c '/usr/share/qa/qa_test_pgbench/postgres/bin/createdb -U postgres pgbench'
        echo $?
	if test $? -eq 0;then
	   PG_DB_CREATED=YES
	   #break
	fi
	
	if test -z ${PG_DB_CREATED};then
	    service_stop
	    _exit 1 "[pg] create db pgbench failed!"
	else
	    echo "[pg] created the db pgbench"
	fi
	
	 echo Initialising database for pgbench: Scale factor $SCALE_FACTOR
	/usr/bin/time -f 'STAT_LOAD %Uuser %Ssystem %Eelapsed' \
	pgbench -U postgres -h $PGHOST -p $PGPORT -i $VACUUM_ARG -s $SCALE_FACTOR pgbench
	if test $? -ne 0;then
	    _exit 1 "pgbench failed to execute!"
	else
	     echo "pgbench default test"
	fi
	                      
	if [ "$CACHE_HOT" != "yes" ]; then
		echo Discarding database cache for cold startup
		service_stop
		                
		echo 3 > /proc/sys/vm/drop_caches
		
		# Starting database
		service_start
 	fi
	
	# Work out max time or max transactions commands
	MAX_TIME_COMMAND= $MAX_TIME
	MAX_TRANSACTIONS_COMMAND=
	
	if [ "$MAX_TIME" != "" ]; then
	   MAX_TIME_COMMAND="-T $MAX_TIME"
	   echo $MAX_TIME > $LOGDIR_RESULTS/pgbench-time
	else
	  if [ "$MAX_TRANSACTIONS" != "" ]; then
	     MAX_TRANSACTIONS_COMMAND="-t $((MAX_TRANSACTIONS/NR_THREADS))"
	  fi
	fi
	
	echo "[pg] starting test cache_hot"
	/usr/bin/time -f 'STAT_LOAD %Uuser %Ssystem %Eelapsed'  \
	  pgbench -U postgres -v -h $PGHOST -p $PGPORT -r -l --aggregate-interval=1  $VACUUM_ARG $READONLY_ARG -c $NR_THREADS \
	                        $MAX_TRANSACTIONS_COMMAND $MAX_TIME_COMMAND pgbench
	if test $? -ne 0;then
	    _exit 1 "pgbench failed to execute cache hot test!"
	else
	     echo "pgbench cache test"
	fi
	
        echo "[pg] dropping the db pgbench"
        su postgres -c '/usr/share/qa/qa_test_pgbench/postgres/bin/dropdb -U postgres pgbench'
        service_stop

done

