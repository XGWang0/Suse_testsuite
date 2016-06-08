#!/bin/bash

qadb_config_set_beijing(){
#/etc/qa/00-qa_tools-default indcate where the reporter
    local _qadb_server_addr
    local _qadb_reporter
    local _config_file
    _config_file="/etc/qa/99-qa_tools-apac2"

    #remove others
    rm "/etc/qa/99-qa_tools-"*
    #to be only one
    cp -v "/etc/qa/00-qa_tools-default" ${_config_file}
    _qadb_server_addr="147.2.207.30"
    _qadb_reporter="rd-qa"
    sed -i "s/^remote_qa_db_report_host=.*$/remote_qa_db_report_host=\"${_qadb_server_addr}\"/g" ${_config_file}
    sed -i "s/^remote_qa_db_report_user=.*$/remote_qa_db_report_user=\"${_qadb_reporter}\"/g" ${_config_file}
}

qadb_config_restore(){
    rm "/etc/qa/99-qa_tools-"*
}

qadb_config_set_beijing
/usr/share/qa/perfcom/perfcmd.py submit-log
qadb_config_restore
/usr/share/qa/perfcom/perfcmd.py compare-log
