#!/bin/python

import time
import sys
import os
import json
import requests

class DDNS(object):

    def __init__(self):
        """Class initialization
        
        Eg. abc.google.com
        
        Args:
            _domain: google.com
            _subdomain: abc
            _token: DNSPOD token. You can fetch this token on the dnspod website(https://www.dnspod.cn/console/user/security).
            _formate: the post format of dnspod. DON'T MODIFIED THE DEFAULT FORMAT.
        """
        self._domain = ''
        self._subdomain = ''
        self._token = ''
        self._format = 'json'

    def getDomainID(self):

        payload = {
            'login_token': self._token,
            'format': self._format
        }
        url = 'https://dnsapi.cn/Domain.List'

        request = self.POST(url, payload)

        if request['status'] != 1:
            raise PostError(request['content'])

        if int(request['content']['status']['code']) != 1:
            raise APIError(request['content']['status']['message'])

        for domain in request['content']['domains']:
            if domain['name'] == self._domain:
                return domain['id']

    def getRecordID(self, domainID):

        payload = {
            'login_token': self._token,
            'format': self._format,
            'domain_id': domainID
        }
        url = 'https://dnsapi.cn/Record.List'

        request = self.POST(url, payload)
        response = {}

        if request['status'] != 1:
            raise PostError(request['content'])

        if int(request['content']['status']['code']) != 1:
            raise APIError(request['content']['status']['message'])

        for record in request['content']["records"]:
            if record["name"] == self._subdomain:
                response["id"] = record["id"]
                response["value"] = record["value"]
                return response

    def updateIP(self, domainID, recordID, hostIP):
        payload = {
            'login_token': self._token,
            'format': self._format,
            'domain_id': domainID,
            'record_id': recordID,
            'sub_domain': self._subdomain,
            'record_line': u'\u9ed8\u8ba4',
            'value': hostIP
        }
        url = 'https://dnsapi.cn/Record.Ddns'

        request = self.POST(url, payload)

        if request['status'] != 1:
            raise PostError(request['content'])

        if int(request['content']['status']['code']) != 1:
            raise APIError(request['content']['status']['message'])

        return 1

    def checkIP(self, recordIP, hostIP):

        if hostIP == recordIP:
            return 0
        else:
            return 1

    def getIP(self):
        payload = {'type': 'ip'}
        url ="https://api.hooowl.com/getIP.php"

        response = self.POST(url, payload)

        if response["status"] != 1:
            raise PostError(response['content'])

        return response['content']['value']

    def POST(self, url, payload):
        response = {}
        try:
            request = requests.post(url, payload, timeout=3)
        except Exception:
            response['status'] = 0
            response['content'] = "Error: connect/post timeout. Please check the domain which must correct."
        else:
            response['status'] = 1
            response['content'] = json.loads(request.text)

        return response

class Log(object):
    def __init__(self):
        pass
    
    def info(self, msg):
        self.checkDir()
        filePath = os.curdir + '/logs/info.log'
        self.writeMsg(filePath, msg)
    
    def error(self, msg):
        self.checkDir()
        filePath = os.curdir + '/logs/error.log'
        self.writeMsg(filePath, msg)
            
    def checkDir(self):
        
        if not os.path.exists(os.curdir + '/logs'):
            os.mkdir(os.curdir + '/logs') 
            
        return 1  
    
    def writeMsg(self, Specfile, msg):   
        try:
            fo = open(Specfile, 'a')
            fo.write(msg + '\n')
            fo.close()
        except Exception:
            pass
        
class Error(Exception):
    """Base class for exception in this module."""
    pass

class APIError(Error):
    """API Error, which is based on the official info."""
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

class PostError(Error):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)

if __name__ == '__main__':
    try:
        dynamic = DDNS()
        logs = Log()
 
        localTime = time.strftime("%a %b %d %H:%M:%S %Y", time.localtime())
        domainid = dynamic.getDomainID()
        record = dynamic.getRecordID(domainid)
        hostIP = dynamic.getIP()
 
        if int(dynamic.checkIP(record['value'], hostIP)) != 1:
            logs.info("[%s] No need to update record IP." % (localTime))
            sys.exit(0)
 
        dynamic.updateIP(domainid, record['id'], hostIP)
 
        logs.info("[%s] The recored IP have updated to be : %s" % (localTime, hostIP))
        
    except PostError as err:
        logs.error("[%s] ERROR: %s" % (localTime, err))

    except APIError as err:
        logs.error("[%s] ERROR: %s" % (localTime, err))

    except Exception as err:
        logs.error("[%s] ERROR: %s" % (localTime, err))
