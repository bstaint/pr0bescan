#/usr/bin/env python
#coding=utf-8
import re,Queue,json
from threading import Thread
from libs.core.common import logging,runtime
from libs.core.common import print_color
from libs.core.network import get
from libs.core.network import tPing

log = logging.getLogger(__name__)

class tThread(Thread):
    def __init__(self,queue,jsons):
        Thread.__init__(self)
        self.queue = queue
        self.jsons = jsons

    def run(self):
        from libs.core.network import get
        while not self.queue.empty():
            path = self.queue.get()
            try:
                code,content = get('dns.aizhan.com',path)
                self.jsons += json.loads(content)
            except:
                continue

def output(target):
    if hasattr(target,'iscdn') and not target.iscdn and target.f_domain:

        threadl = jsons = []; threads = 5   # 线程数

        queue=Queue.Queue()

        print_color('find domain in same IP for %s..'%target.ip, 2)

        code,content = get('dns.aizhan.com','/index.php?r=index/pages&q=%s' % target.f_domain)
        match = re.search('1/(\d{1,})', content)

        page = int(match.group(1)) if match else 1
        # 多线程翻页获取同IP域名，
        [queue.put('/index.php?r=index/getress&q=%s&page=%d' % (target.f_domain,i)) for i in xrange(1,page+1)]
        threadl = [tThread(queue,jsons) for x in xrange(0, threads)]
        [t.start() for t in threadl]
        [t.join() for t in threadl]

        #Ping IP
        [queue.put(json['domain']) for json in jsons]
        threadl = [tPing(queue,target.ip) for x in xrange(0, threads)]
        [t.start() for t in threadl]
        [t.join() for t in threadl]
       
        print('')
