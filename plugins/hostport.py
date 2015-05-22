#/usr/bin/env python
#coding=utf-8
import Queue
from threading import Thread
from libs.core.common import logging,runtime
from libs.core.common import print_color
from libs.core.network import tPort

log = logging.getLogger(__name__)

def output(target):
    if hasattr(target,'iscdn') and not target.iscdn:

        Ports=[21,22,23,25,80,81,110,135,139,389,443,445,873,1433,1434,1521,2433,3306,3307,3366,3336,3380,3389,3968,5800,5900,7755,8000,8001,8002,8080,8650,8888,8800,9999,12580,22222,22022,27017,28017,33089,34567,43958,50001]

        print_color('scan port for IP %s..'%target.ip, 2)

        threadl = []; threads = 20
        queue=Queue.Queue()

        [queue.put({'ip':target.ip,'port':port}) for port in Ports]
        threadl = [tPort(queue) for x in xrange(0, threads)]
        [t.start() for t in threadl]
        [t.join() for t in threadl]
        
        print('')

