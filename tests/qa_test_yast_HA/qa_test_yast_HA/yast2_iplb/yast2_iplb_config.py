# -*- coding: utf-8 -*-
# ****************************************************************************
# Copyright (c) 2011 Unpublished Work of SUSE, Inc. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE, INC.  IT CONTAINS SUSE'S
# CONFIDENTIAL, PROPRIETARY, AND TRADE SECRET INFORMATION.  SUSE
# RESTRICTS THIS WORK TO SUSE EMPLOYEES WHO NEED THE WORK TO PERFORM
# THEIR ASSIGNMENTS AND TO THIRD PARTIES AUTHORIZED BY SUSE IN WRITING.
# THIS WORK IS SUBJECT TO U.S. AND INTERNATIONAL COPYRIGHT LAWS AND
# TREATIES. IT MAY NOT BE USED, COPIED, DISTRIBUTED, DISCLOSED, ADAPTED,
# PERFORMED, DISPLAYED, COLLECTED, COMPILED, OR LINKED WITHOUT SUSE'S
# PRIOR WRITTEN CONSENT. USE OR EXPLOITATION OF THIS WORK WITHOUT
# AUTHORIZATION COULD SUBJECT THE PERPETRATOR TO CRIMINAL AND  CIVIL
# LIABILITY.
# 
# SUSE PROVIDES THE WORK 'AS IS,' WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY, INCLUDING WITHOUT THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, AND NON-INFRINGEMENT. SUSE, THE
# AUTHORS OF THE WORK, AND THE OWNERS OF COPYRIGHT IN THE WORK ARE NOT
# LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION
# WITH THE WORK OR THE USE OR OTHER DEALINGS IN THE WORK.
# ****************************************************************************

# Machines settings
real_server1 = "147.2.207.3"
real_server2 = "147.2.207.4"
virtual_server = "147.2.207.5"

# Global configuration settings:
gt_check_interval = "5"
gt_check_timeout = "3"
gt_failure_count = ""
gt_negotiate_timeout = ""
gt_fallback = ""
gt_log_file = "/var/log/ldirectord.log"
gt_email_alert = ""
gt_email_alert_freq = ""
gt_email_alert_status = ""
gt_callback = ""
gt_execute = ""
gc_auto_reload = "yes"
gc_quiescent_fork = "yes"
gc_fork = ""
gc_supervised = ""

# Virtual Server configuration settings:
vt_virtual_server = "147.2.207.5:80"
real_server_1 = "147.2.207.3:80"
real_server_2 = "147.2.207.4:80"
vc_check_type = "negotiate"
vc_service = "http"
vt_check_command = ""
vt_check_port = ""
vt_request = "test.html"
vt_receive = "still alive"
vc_http_method = ""
vt_virtual_host = ""
vt_login = ""
vt_password = ""
vt_database_name = ""
vt_radius_secret = ""
vt_persistent = ""
vt_netmask = ""
vc_scheduler = "wlc"
vc_protocol = "tcp"
vt_check_timeout = ""
vt_negotiate_timeout = ""
vt_failure_count = ""
vt_email_alert = ""
vt_email_alert_freq = ""
vc_email_alert_status = ""
vt_fallback = "127.0.0.1:80"
vc_quiescent = ""
