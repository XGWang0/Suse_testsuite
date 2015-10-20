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

import random
import time
from urllib2 import urlopen, HTTPError, Request

from constantvars import LOGGER

class URLParser(object):
    
    def __init__(self):
        pass

    @staticmethod
    def checkURLPath(url, times=1):
        for i in range(times):
            try:
                # Solve the server socket down issue
                urlq = Request(url, headers={'User-Agent':''.join(random.sample('zyxwvutsrqponmlkjihgfedcba',5))})
                w = urlopen(urlq)
                return True
            except HTTPError,e:
                if i == times-1:
                    LOGGER.warn("URL [%s] %s" %(url,e) )
                    return False
                else:
                    time.sleep(3)
                    continue
            except Exception, e:
                if i == times-1:
                    LOGGER.warn("URL [%s] %s" %(url,e) )
                    return False
                else:
                    time.sleep(3)
                    continue

    def getValidURL(self, url):
        convert_url_flag = False
        while True:
            if URLParser().checkURLPath(url):
                return url
            else:
                if convert_url_flag is True:
                    break
                if 'dvd' in url:
                    url = url.replace('dvd1','DVD1')
                    convert_url_flag = True
                    LOGGER.info("Try to convert url to %s" %url)
                elif 'DVD' in url:
                    url = url.replace('DVD1','dvd1')
                    convert_url_flag = True
                    LOGGER.info("Try to convert url to %s" %url)
                else:
                    print "url does not exist"
                    return ""
        
        return ""
    
    def getFileContent(self,url, times=3):
        
        for i in range(times):
            url = self.getValidURL(url)
            if not url:
                return ""
            
            try:
                w = urlopen(url)
                r =  w.read()
                return r
            except HTTPError,e:
                LOGGER.error(e)
                if i == 2:
                    return ""
                else:
                    time.sleep(1)
                    continue
            except URLError, ex:
                LOGGER.error(ex)
                if i == 2:
                    return ""
                else:
                    time.sleep(1)
                    continue         
            finally:
                pass
                #w.close()
