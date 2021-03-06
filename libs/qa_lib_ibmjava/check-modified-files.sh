#!/bin/bash

# this script will go through installed files and check the filelists
# TODO: -32bit packages are not nested!

# https://wiki.innerweb.novell.com/index.php/RD-OPS_QA/Automation/Handbook/Packaging#Return_Codes
E_PASSED=0
E_FAILED=1
E_ERROR=11
E_SKIPPED=22

function error() {

    echo "${@}" >&2

}

function ecat() {

    cat "${@}" >&2

}

function usage() {

    error "Usage: ${0} jdk-version"
    error "where jdk-version is identifier of major jdk version <4;6>"
    error "it's free-form, so values like jdk4, java6, or 5 are allowed"
    error "variants like -32bit or -sap packages are already suported (jdk4-sap)"
}

function parse_args() {

    if [[ -z "${1}" ]]; then
        usage "${0}"
        exit ${E_ERROR}
    fi

    case "${1}" in
        *4*)
            MAIN_PACKAGE="java-1_4_2-ibm"
            ;;
        *5*)
            MAIN_PACKAGE="java-1_5_0-ibm"
            ;;
        *6*)
            MAIN_PACKAGE="java-1_6_0-ibm"
            ;;
        *7.1*|*7_1*)
            MAIN_PACKAGE="java-1_7_1-ibm"
            ;;
        *7*)
            MAIN_PACKAGE="java-1_7_0-ibm"
            ;;
        *8*)
            MAIN_PACKAGE="java-1_8_0-ibm"
            ;;
        *)
            error "Unkown value ${1}"
            usage "${0}"
            exit ${E_ERROR}
            ;;
    esac

    if   [[ "${1}" =~ -32bit$ ]]; then
        MAIN_PACKAGE=${MAIN_PACKAGE}-32bit
    elif [[ "${1}" =~ -sap$ ]]; then
        MAIN_PACKAGE=${MAIN_PACKAGE}-sap
    fi

}

function is_package_installed() {

    rpm --quiet -q "${1}"

}

function get_qa_filelist() {

    local ret

    ret=$(rpm -ql ${1} | grep qa_filelist)

    if [[ -n ${ret} && -f ${ret} ]]; then
        QA_FILELIST=${ret}
        return 0
    fi

    return 1

}

function get_packages_from_filelist() {
    cat ${1} | cut -d ';' -f 4 | sort -u
}

# perform the QA check - it eats following arguments
# package - package name
function check() {

    local main_package qa_filelist
    local tempfile errfile

    main_package=${1}
    qa_filelist=${2}


    for package in $(get_packages_from_filelist "${qa_filelist}"); do

        tempfile=check_filelist.${package}
        stdout=md5sum_stdout.${package}
        stderr=md5sum_stderror.${package}

        # make qa_filelist md5sum compatible
        grep "${package}$" "${qa_filelist}"  | cut -d ';' -f 1,3 | sed 's@;@  /@' > "${tempfile}"
        
        exec 3> "${stdout}"
        exec 4> "${stderr}"
        
        if ! md5sum -c ${tempfile} >&3 2>&4; then
            # the md5sum ends with an error
            if [[ $(grep "No such file or directory" "${stderr}" | wc -l) == $(wc -l < "${tempfile}") ]]; then
                # but not for a subpackage as it can be intentional
                error "WARNING: ${package} is not installed, skipping the check"
                continue
            fi
            # the "file" is actualy a symlink generated later on and thus
            # we get "Is a directory" which we can skip
            if [[ $(grep "Is a directory" "${stderr}" | wc -l) > 0 ]]; then
                echo "INFO: ${package} contains file converted to symlink (Is a drectory md5sum report):"
                cat "${stderr}"
		continue
            fi

            # md5sum does not match - this is serious error
            error "ERROR: md5sum for ${package} have failed"
            grep 'FAILED$' "${stdout}" >&2
            ecat "${stderr}"
            exit ${E_ERROR}
        fi

    done

    return 0
}

export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8

function main() {

    local tmpdir subdir

    MAIN_PACKAGE=
    QA_FILELIST=

    parse_args "${@}"

    if [[ -z "${MAIN_PACKAGE}" ]]; then
        error "ERROR: cannot parse jdk version"
        exit ${E_ERROR}
    fi

    if ! is_package_installed "${MAIN_PACKAGE}"; then
        error "ERROR: ${MAIN_PACKAGE} is not installed, cannot perform the test!"
        exit ${E_ERROR}
    fi

    if ! get_qa_filelist "${MAIN_PACKAGE}"; then
        error "ERROR: cannot get a location of .qa_filelist"
        error "${MAIN_PACKAGE} is not yet prepared for the QA check?"
        exit ${E_ERROR}
    fi

    if [[ -n "${QADEBUG}" ]]; then
        # non-secure but debuggable temp dir
        error "WARNING: QADEBUG is set, using local tmp dir as the working one"
        rm -rf tmp || exit ${E_ERROR}
        mkdir -p tmp || exit ${E_ERROR}
        if [[ ! -d tmp ]]; then
            error "ERROR: tmp is not a directory!"
            exit ${E_ERROR}
        fi
        tmpdir="tmp"
    else
        tmpdir=$(/bin/mktemp -d ${TMPDIR:-/tmp}/check-modified-files.XXXXXXXXXXXX)
        trap "rm -rf ${tmpdir}" EXIT TERM INT
    fi

    pushd ${tmpdir} &>/dev/null

    check "${MAIN_PACKAGE}" "${QA_FILELIST}"
    
    popd &> /dev/null
    
    if [[ -z "${QADEBUG}" ]]; then
        rm -rf "${tmpdir}"
    fi

}

main "${@}"
