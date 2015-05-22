#!/usr/bin/env python
# -*- coding: utf-8 -*-
from urlparse import urlparse

from common import *
from os.path import split
from network import head, ping, valid_ip

from libs.pythonwhois import extract_domain
from libs.utils import import_string, find_modules

log = logging.getLogger(__name__)

class Pr0beScan:

    prots = {'http':80, 'https':443}

    header = {}

    f_domain = n_domain = False

    # 执行插件
    def plugin(self,name):
        plugin = import_string(name, silent=True)
        plugin.output(self) if plugin else None

    # 输出基本信息
    def print_info(self):
        print_color('IP: %s'%self.ip, 1)

        if self.f_domain:
            print_color('Domain: %s'%self.f_domain, 1)

        if 'server' in self.header and len(self.header['server']):
            print_color('Server: %s'%self.header['server'], 1)

        print('')

    # 解析URL
    def urlparse(self,url):
        urls = urlparse(url)

        if urls.scheme in self.prots.keys():
            self.protocol = urls.scheme
            purl = urls.netloc.split(':')
            
            self.port = int(purl[1]) if len(purl) == 2 else self.prots[self.protocol]

            self.path = split(urls.path)[0] if urls.path != '' else '/'

            if not valid_ip(purl[0]):
                self.f_domain = purl[0]
                self.ip = ping(self.f_domain)

            return True
        else:
            return False

    # 探测基本信息
    def probe(self,url):
        try:
            if self.urlparse(url):

                if self.f_domain:
                    domain = '%s:%d' % (self.f_domain, self.port)
                else:
                    domain = '%s:%d' % (self.ip, self.port)

                self.code,self.header = head(domain, self.path, self.protocol)
                
                if self.f_domain:
                    self.n_domain = extract_domain(self.f_domain)

                return True
            else:
                return False
        except:
            log.exception('exception')
            return False
