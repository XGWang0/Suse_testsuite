#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE, Inc. All Rights Reserved.
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

import os

# Machines settings
sys1_eth0_ip = os.popen('ifconfig |grep -F addr: |cut -d : -f 2 |cut -d " " -f 1').read().strip()
sys1_root_pwd = ""

sys2_eth0_ip = ""

# Wireless settings
wireless1_name = "SLEDQATEAM-DLINK"
wireless1_pwd = "aaaaaaaaaa"

wireless2_name = "SLEDQATEAM_LINKSYSWLAN_TEST"
wireless2_pwd="sledqateam"

# VPN settings
vpn_user_name = ""
vpn_user_pwd = ""
vpn_gateway = ""
vpn_group_name = ""
vpn_group_pwd = ""

# Static network settings
static_ip = "147.2.212.199"
static_dns = "202.106.0.20"
static_mask = "255.255.255.0"
static_gateway = "147.2.212.254"

# Hidden Wireless settings
hidden_wireless_name = "SLEDQATEAM-DLINK"
hidden_wireless_pwd = "aaaaaaaaaa"
hidden_wireless_dns = "192.168.0.1"

# D-LINK SYSTEM settings
dlink_url = "http://192.168.0.1"
admin_pwd = ""

# Novell secure wifi settings
wifi_user_name = ""
wifi_user_pwd = ""

# Wireless security methods settings
WEP40bit_net_name = ""
WEP40bit_key = ""
WEP128bit_net_name = ""
WEP128bit_key = ""
LEAP_net_name = ""
LEAP_user_name = ""
LEAP_user_pwd = ""
Dynamic_net_name = ""
Dynamic_key_pwd = ""

# openVPN connection settings
crt_download_url = "http://147.2.207.138/client1.tgz"
openvpn_gateway = "147.2.207.138"
user_crt = "client1.crt"
ca_crt = "ca.crt"
private_key = "client1.key"
vpn_dns = "10.8.0.1"
