#/usr/bin/env python
#coding=utf-8
import Queue
from threading import Thread
from libs.core.common import logging,runtime
from libs.core.common import print_color,query_yes_no
from libs.core.network import tPort

log = logging.getLogger(__name__)

def output(target):

    if query_yes_no('subnet port scan requires a lot of time.'):

        Ports=[80,8000,8080,88]
        threadl = [];threads = 20
        queue=Queue.Queue()

        print_color('scan port for subnet %s..'%target.ip, 2)

        subnet = ['%s.%d' % (target.ip[0:target.ip.rfind('.')],i) for i in range(1,255)]

        for port in Ports:
            for sub in subnet:
                queue.put({'ip':sub,'port':port})

        threadl = [tPort(queue) for x in xrange(0, threads)]
        [t.start() for t in threadl]
        [t.join() for t in threadl]
    
    print('')
