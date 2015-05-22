#/usr/bin/env python
#coding=gbk
import json
from libs.core.network import get
from libs.core.common import logging,runtime
from libs.core.common import print_color

log = logging.getLogger(__name__)

def output(target):
    print_color('get location for IP %s' % target.ip, 2)
    try:
        code,content = get('ip.taobao.com', '/service/getIpInfo.php?ip=%s' % target.ip)
        jsons = json.loads(content)
        print_color('%s %s %s %s'%(jsons['data']['country'].encode('gbk'),
            jsons['data']['region'].encode('gbk'),
            jsons['data']['city'].encode('gbk'),
            jsons['data']['isp'].encode('gbk')), 1)
    except:
        log.exception('exception')
        print_color(__name__+' faild', 0)

    print('')
