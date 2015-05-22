#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import httplib
import urllib
import Queue
from common import *
from threading import Thread

socket.setdefaulttimeout(5)
log = logging.getLogger(__name__)

headers = { 
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.146 Safari/537.36', 
            'referer':'http://www.google.com.hk/'
        }

def valid_ip(ip):
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

# HEAD请求
def head(domain,path,protocol='http'):
    if protocol == 'http':
        conn = httplib.HTTPConnection(domain)
    elif protocol == 'https':
        conn = httplib.HTTPSConnection(domain)
    else:
        return 
    conn.request('HEAD',path,headers=headers)
    response = conn.getresponse()
    code = response.status
    header = dict(response.getheaders())
    return code,header 

# HEAD请求
def get(domain,path,protocol='http'):
    if protocol == 'http':
        conn = httplib.HTTPConnection(domain)
    elif protocol == 'https':
        conn = httplib.HTTPSConnection(domain)
    else:
        return 
    conn.request('GET',path,headers=headers)
    response = conn.getresponse()
    code = response.status
    content = response.read()
    return code,content


def post(domain,path,data,protocol='http'):
    if protocol == 'http':
        conn = httplib.HTTPConnection(domain)
    elif protocol == 'https':
        conn = httplib.HTTPSConnection(domain)
    else:
        return 
    data = urllib.urlencode(data)
    conn.request('POST',path,data,headers=headers)
    response = conn.getresponse()
    code = response.status
    content = response.read()
    return code,content

# PING
def ping(domain):
    return socket.gethostbyname(domain)


class tPort(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while not self.queue.empty():
            try:
                task = self.queue.get()
                task_count = self.queue.qsize()
                if (task_count % 100) == 0 and task_count != 0:
                    print_color('last %d tasks' % task_count, 2)
                sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sk.connect((task['ip'] ,task['port']))
                print_color('%s %s' % (task['ip'], task['port']), 1)
            except:
                continue

class tPing(Thread):

    def __init__(self,queue,ip):
        Thread.__init__(self)
        self.queue = queue
        self.ip = ip

    def run(self):
        while not self.queue.empty():
            domain = self.queue.get()
            try:
                ip  = ping(domain)
                if ip == self.ip:
                    msg = '%s *'%domain
                # subnets mark *
                elif ip[0:ip.rfind('.')] == self.ip[0:self.ip.rfind('.')]:
                    msg = '%s %s *'%(domain,ip)
                else:
                    msg = '%s %s'%(domain,ip)
                print_color(msg, 1)
            except:
                log.exception('exception')
                continue
