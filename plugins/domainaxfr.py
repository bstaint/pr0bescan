#/usr/bin/env python
#coding=utf-8
from libs.core.common import logging,runtime
from libs.core.common import print_color
from libs.core.network import valid_ip
import libs.DNS as DNS

log = logging.getLogger(__name__)

def parse_record(records,ip):
    for record in records:
        if type(record) is dict\
        and type(record['data']) is str\
        and valid_ip(record['data']):
            if record['data'] == ip:
                print_color('%s *'%(record['name']), 1)
            else:
                print_color('%s %s'%(record['name'],record['data']), 1)

def output(target):
    if target.n_domain:

        target.axfr = False
        print_color('Test AXFR request for %s' % target.n_domain, 2)

        try:
            # get dns domain
            r = DNS.DnsRequest(target.n_domain, qtype="NS", server=['223.5.5.5'], protocol='udp', timeout=10)
            res = r.req().answers
            for r in res:
                dns = r['data']
                print_color('Test DNS %s' % dns, 2)
                r = DNS.DnsRequest(target.n_domain, qtype="AXFR", server=[dns], protocol='tcp', timeout=10)
                res = r.req()
                if len(res.answers) > 0:
                    target.axfr = True
                    parse_record(res.answers,target.ip)
                    break
        except:
            log.exception('exception')
        
        print('')
