### setup an import mechanism
function __import {
    # NOTE absolute path is not supported.
    local _lock
    local lib
    if test "X${__IMPORT_ROOT}" == "X";then
        echo "[IMPORT] ERROR __IMPORT_ROOT is NULL"
        exit 1
    fi
    if echo $1 | egrep -q '^/'; then
        lib=$1
    else
        lib=${__IMPORT_ROOT}/$1
    fi
    _lock=$(echo $1 | tr '[a-z./\-]' '[A-Z___]')
    if eval "test X\$${_lock}_IMPORTED != XYES";then
        if test -f ${lib}; then
            echo "[IMPORT] [debug] source ${lib}"
            source ${lib}
            eval "readonly ${_lock}_IMPORTED=YES"
        else
            echo [import] "lib dose NOT exist ${lib}"
            return 2
        fi
    else
        : echo "[IMPORT] $1 has already been imported!"
    fi
}
