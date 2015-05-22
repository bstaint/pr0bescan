#/usr/bin/env python
#coding=utf-8
import Queue
from re import findall
from libs.core.common import logging,runtime
from libs.core.common import print_color
from libs.core.network import tPing
from libs.core.network import get

log = logging.getLogger(__name__)

def output(target):
    if hasattr(target,'mail'):
        print_color('whois same mail %s domain ...' % target.mail, 2)

        threadl = []; threads = 5

        queue = Queue.Queue()
        try:
            code,content = get('whois.aizhan.com',
                               '/reverse-whois/?q=%s&t=email' % target.mail)
            domain_list = findall(r'_blank">(.*?)</a></td>', content)
            if len(domain_list):
                [queue.put(domain) for domain in domain_list if domain != target.n_domain]
                threadl = [tPing(queue,target.ip) for x in xrange(0, threads)]
                [t.start() for t in threadl]
                [t.join() for t in threadl]
        except:
            log.exception('exception')
            print_color(__name__+' faild', 0)

        print('')
        
