#/usr/bin/env python
#coding=utf-8
from re import search
from libs.core.network import head,get 
from libs.core.common import logging,runtime
from libs.core.common import print_color

log = logging.getLogger(__name__)

def output(target):
    powereds = [{'type':'ASP/ASPX','str':'ASP.NET'}, {'type':'PHP','str':'PHP/'}]

    scripts = [
                {'type':'ASP','path':'/index.asp'}, 
                {'type':'ASPX','path':'/index.aspx'},
                {'type':'PHP','path':'/index.php'}
            ]

    searchs = [
                {'type':'ASP','path':'/search?q=site:%s+inurl:asp'},
                {'type':'ASPX','path':'/search?q=site:%s+inurl:aspx'},
                {'type':'PHP','path':'/search?q=site:%s+inurl:php'}
            ]

    domain = '%s:%d' % (target.f_domain, target.port) if target.f_domain else '%s:%d' % (target.ip, target.port)
    print_color('Probe website %s script...'%domain, 2)
    target.script = 'unknown'

    if 'x-powered-by' in target.header:
        print_color('Test Script for %s with X-Powered-By'%target.f_domain, 2)
        for item in powereds:
            if item['str'] in target.header['x-powered-by']:
                target.script = item['type']
                break

    try:
        if target.script == 'unknown':
            print_color('Test script for %s with HTTP header'%target.f_domain, 2)
            for item in scripts:
                code,header = head(domain,item['path'],target.protocol)
                if code == 200:
                    target.script = item['type']
                    break


        if target.script == 'unknown':
            print_color('Test script for %s with search engine'%target.f_domain, 2)
            for item in searchs:
                path = item['path'] % target.f_domain if target.f_domain else item['path'] % target.ip
                code,content = get('www.google.com.hk',path)
                match = search(r'resultStats">(.*?)<nobr>', content)
                if match:
                    target.script = item['type']
    except:
        log.exception('exception')
        print_color(__name__+' faild', 0)
    
    print_color(target.script, 1)
    print('')
