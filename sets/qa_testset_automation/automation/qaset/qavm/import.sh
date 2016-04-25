### setup an import mechanism
function __import {
    # NOTE absolute path is not supported.
    local _lock
    local lib
    if test "X${__IMPORT_ROOT}" == "X";then
        echo "[IMPORT] ERROR __IMPORT_ROOT is NULL" >&2
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
            echo "[IMPORT] [debug] source ${lib}" >&2
            source ${lib}
            eval "readonly ${_lock}_IMPORTED=YES"
        else
            echo "[IMPORT] lib dose NOT exist ${lib}" >&2
            return 2
        fi
    else
        : echo "[IMPORT] $1 has already been imported!" >&2
    fi
}
