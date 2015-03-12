#!/bin/bash

hook_debug(){
    true
}

sq_hook_list_new(){
    local _name
    _name=$1
    declare -a SQ_HOOK_LIST_${_hook_list}
}

sq_hook_list_append(){
    local _name=$1
    local _func=$2

    eval "SQ_HOOK_LIST_${_name}=(\${SQ_HOOK_LIST_${_name}[@]} ${_func})"
    hook_debug && {
        echo ${FUNCNAME} SQ_HOOK_LIST_${_name}
        eval "echo \${SQ_HOOK_LIST_${_name}[@]}"
    }
}

sq_hook_list_remove(){
    local _name=$1
    local _func=$2

    eval "SQ_HOOK_LIST_${_name}=(\${SQ_HOOK_LIST_${_name}[@]/${_func}/})"
    hook_debug && {
        echo ${FUNCNAME} SQ_HOOK_LIST_${_name}
        eval "echo \${SQ_HOOK_LIST_${_name}[@]}"
    }
}

sq_hook_list_foreach(){
    local _list
    local _name=$1
    local _func

    hook_debug && {
        echo ${FUNCNAME} SQ_HOOK_LIST_${_name}
    }

    eval "_list=(\${SQ_HOOK_LIST_${_name}[@]})"
    for _func in ${_list[@]};do
        ${_func}
    done
}
