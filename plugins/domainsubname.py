#/usr/bin/env python
#coding=utf-8
from libs.core.common import logging,runtime
from libs.core.common import print_color
from libs.core.network import get,post
from libs.core.network import tPing
from re import findall
import Queue

log = logging.getLogger(__name__)

def output(target):
    if hasattr(target,'axfr') and not target.axfr and target.n_domain:

        threadl = [];threads = 5

        queue = Queue.Queue()

        apis = [{'domain':'www.baidu.com',
                'path':'/s?wd=site:%s&pn=0&ie=utf-8' % target.n_domain,
                'method':'get',
                'regex':'"g">(.*?)%s'%target.n_domain},
                {'domain':'i.links.cn',
                'path':'/subdomain/',
                'method':'post',
                'regex':'target=_blank>http://(.*)%s',
                'data':{'domain':target.n_domain,'b2':'1','b3':'1','b4':'1'}},
                {'domain':'www.alexa.com',
                'path':'/siteinfo/%s' % target.n_domain,
                'method':'get',
                'regex':"word-wrap'>(.*?)%s"%target.n_domain}]
        
        print_color('find subdomain for %s..' % target.n_domain, 2)

        pix_list = []

        try:
            for api in apis:
                try:
                    if api['method'] == 'get':
                        code,content = get(api['domain'],api['path'])
                        pix_list += findall(api['regex'], content)
                    elif api['method'] == 'post':
                        code,content = post(api['domain'],api['path'],api['data'])
                        pix_list += findall(api['regex'], content)
                except:
                    print_color(api['domain']+' Faild', 0)

            pix_list = {}.fromkeys(pix_list).keys()

            for pix in pix_list:
                queue.put('%s%s'%(pix,target.n_domain))
            
            threadl = [tPing(queue,target.ip) for x in xrange(0, threads)]
            [t.start() for t in threadl]
            [t.join() for t in threadl]
        except:
            log.exception('exception')
            print_color(__name__+' faild', 0)

        print('')

