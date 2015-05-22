#/usr/bin/env python
#coding=utf-8
import re
from libs.core.common import logging,runtime
from libs.core.common import print_color
from libs.core.network import get,head

log = logging.getLogger(__name__)

def output(target):
    print_color('Test server exploit %s...'%target.ip, 2)

    paths = ['/robots.txt/.php', '/robots.txt/1.php']

    if 'server' in target.header:
        server = target.header['server'].lower()
        if 'nginx' in server:

            target.server = 'Nginx'

            print_color('Test server nginx Parsing Vulnerabilities',2)

            domain = '%s:%d' % (target.f_domain, target.port) if target.f_domain else '%s:%d' % (target.ip, target.port)

            code,content = get(domain, '/')
            match = re.search(r'src="(http.+?\.jpg)"', content)

            if match:
                paths.append('%s/.php' % match.group(1))
                paths.append('%s/1.php' % match.group(1))
            for p in paths:
                code,header = head(domain,p)

                if code == 200 and header['content-type'].find('text/html') > -1:
                    print_color('the server has nginx parsing vulnerabilities',1)
                    break

        elif 'apache' in server:
            target.server = 'Apache'
        elif 'iis' in server:
            target.server = 'IIS'

    print('')
