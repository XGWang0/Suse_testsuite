#!/bin/bash
# ****************************************************************************
# Copyright (c) 2013 Unpublished Work of SUSE. All Rights Reserved.
# 
# THIS IS AN UNPUBLISHED WORK OF SUSE.  IT CONTAINS SUSE'S
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
#

source testlib.sh
assert_root

NEW_REPO_NAME='qa_test2'

#Add a repo.
assert_result "ar $REPO $REPO_NAME" "Repository '$REPO_NAME' successfully added"

#Rename repo.
assert_result "nr $REPO_NAME $NEW_REPO_NAME" "Repository '$REPO_NAME' renamed to '$NEW_REPO_NAME'."

#List repos.
assert_result "lr" "$NEW_REPO_NAME"
assert_output "lr" "repos"

#Disable repo.
assert_result "mr -d $NEW_REPO_NAME" "Repository '$NEW_REPO_NAME' has been successfully disabled."

#Enable repo.
assert_result "mr -d $NEW_REPO_NAME" "Repository '$NEW_REPO_NAME' has been successfully enabled."

#Remove a repo.
assert_result "rr $NEW_REPO_NAME" "Repository '$NEW_REPO_NAME' has been removed."

#Refresh repos.
assert_result "ref" "All repositories have been refreshed."

echo "Test completed successfully" 

