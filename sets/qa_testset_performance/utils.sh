function sq_msg {
    local lv=$1
    shift
    local prefix

    case ${lv} in
        Error*)
            prefix="\033[0;31mERROR\033[0m"
            ;;
        Info*)
            prefix="\033[0;33mINFO\033[0m"
            ;;
        Warn*)
            prefix="\033[0;35mWARN\033[0m"
            ;;
        Debug*)
            prefix="\033[0;32mDEBUG\033[0m"
            ;;
        *) # not a proper one
            prefix="\033[0;31m${lv}\033[0m"
            ;;
    esac
    echo -e "[SLE-QA] ${prefix}\t$1"
    shift
    while test $# -gt 0; do
        echo -e "\t\t$1"
        shift
    done
}

function sq_debug {
    if test "X${SQ_DEBUG_ON}" == "XYES"; then
        sq_msg Debug "$@"
    fi
}

function sq_info {
    sq_msg Info "$@"
}

function sq_warn {
    sq_msg Warn "$@"
}

function sq_error {
    sq_msg Error "$@"
}

function sq_assert {
    sq_msg Assert "$@"
    exit 4
}

### add and ref necessary repos
# arch
# release
# repo_server
function sq_prep_repos {
    local _arch=$1
    local _SLE_build=$2
    local _repo_mirror=$3

    local _repo_url
    local _repo_name
    local _repos_num

    _repos_num=${#SQ_REPO_NAMES[*]}
    if test $_repos_num -le 0;then
        sq_warn "There is NO repo to be added." \
            "Please check the conf file!"
        return 1  ## no repo to be added
    else
        sq_info "There are ${_repos_num} repos to be added."
    fi

    for _repo_name in ${SQ_REPO_NAMES[*]};do
        _repo_url=$(sq_prep_${SLE_RELEASE}_get_repo_url_by_name ${_repo_name} ${_SLE_build} ${_arch} ${_repo_mirror})
        sq_info "add and ref repo" \
            "${_repo_name}" \
            "${_repo_url}"
        #delete the old one
        ${SQ_DEBUG_ECHO} zypper rr ${_repo_name}
        ${SQ_DEBUG_ECHO} zypper --no-gpg-checks -n ar ${_repo_url} ${_repo_name}
        if [ $? != 0 ];then
            sq_error "zypper add repo ${_repo_name} failed." \
                "The URI is\n\t${_repo_url}"
            return 2 #return or exit ??
        fi
        ${SQ_DEBUG_ECHO} zypper --gpg-auto-import-keys ref ${_repo_name}
        if [ $? != 0 ];then
            sq_error "zypper refresh repo ${_repo_name} failed." \
                "Check the connection to server"
            return 3
        fi
    done
    return 0
}

function sq_prep_install_packages_qa_libs {
    if test ${#SQ_LIBS[*]} -le 0;then
        sq_error "The SQ_LIBS has no packages!" \
            "Please check the conf file"
        return 1
    fi
    ${SQ_DEBUG_ECHO} zypper -n in -l ${SQ_LIBS[*]}
    if [ $? != 0 ];then
        sq_error "install packages for qa_LIBS failed!"
        return 2
    fi
    return 0
}

function sq_prep_install_packages_component {
    local _com=$1
    if eval "test \${#SQ_CMPNT_${_com}[*]} -le 0";then
        sq_error "The component ${_com} has no packages!" \
            "Please check the conf file"
        return 1
    fi
    sq_info "Try to install packages for ${_com}"
    eval "${SQ_DEBUG_ECHO} zypper -n in -l \${SQ_CMPNT_${_com}[*]}"
    if [ $? != 0 ];then
        sq_error "install packages for $_COM failed\n"
        return 2
    fi
    return 0
}

function sq_prep_repos_and_packages {
    local _arch=$1
    local _SLE_build=$2
    local _repo_mirror=$3

    sq_prep_repos ${_arch} ${_SLE_build} ${_repo_mirror} && \
        sq_prep_install_packages_qa_libs && \
        sq_prep_install_packages_component performance
#        sq_prep_install_packages_component performance && \
#        sq_prep_install_packages_component regression && \
#        sq_prep_install_packages_component acceptance && \
#        sq_prep_install_packages_component kernel && \


    if test $? -ne 0;then
        exit 5
        rm -f ${_autorun_lock}
    fi
}
