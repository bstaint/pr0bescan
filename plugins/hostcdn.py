#/usr/bin/env python
#coding=utf-8
from libs.core.common import logging,runtime
from libs.core.common import print_color
import libs.DNS as DNS

log = logging.getLogger(__name__)

def output(target):
    customHeaders = ['x-powered-by-360wzb',
            'x-powered-by-anquanbao','x-cache','webluker-edge',
            'powered-by-chinacache']

    cnames = ['360wzb','incapdns','aqb.so']

    target.iscdn = False

    print_color('Test CDN for %s'%target.ip, 2)
    print_color('Test CDN for %s with HTTP header'%target.f_domain, 2)

    if any('cdn' in header for header in target.header):
        target.iscdn = True

    if not target.iscdn:
        flag = set(target.header).intersection(set(customHeaders))
        target.iscdn = True if len(flag) else None

    if not target.iscdn and target.f_domain:
        try:
            print_color('Test CDN for %s with CNAME'%target.f_domain, 2)
            r = DNS.DnsRequest(target.f_domain, qtype="CNAME", 
                    server=['8.8.8.8'], protocol='tcp', timeout=10)
            res = r.req()
            if len(res.answers) > 0:
                cname = res.answers[0]['data']
                # 值得学习
                if any(cname_str in cname for cname_str in cnames):
                    target.iscdn = True
        except:
            log.exception('exception')
            print_color(__name__+' faild', 0)

    if target.iscdn:
        print_color(target.iscdn, 1)
    
    print('')
