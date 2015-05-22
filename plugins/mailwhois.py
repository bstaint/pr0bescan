#/usr/bin/env python
#coding=utf-8
from re import findall
from libs.core.common import logging,runtime
from libs.core.common import print_color
from libs.pythonwhois import get_whois

log = logging.getLogger(__name__)
    
keywords = ['whoisprivacyprotect', 'webnic.cc', 'sudu.cn', 'markmonitor', 'godaddy', 'everdns.com', 'bizcn.com', 'whoisprotectionservice', 'sun-privacy', 'xinnet.com', 'zhujiwu.com', 'west263.com', 'enom.com', 'privacyguardian', 'zgsj.com', '1api.net', 'nsi_domainadmin', 'changer.cn', 'hichina.com', 'list.alibaba-inc.com', 'name.com', 'protecteddomainservices.com', '53dns.com', 'abuse@dns.com.cn', 'yovole.com', 'ce.net.cn', '8ycn.com']

def filter_mail(mail):
    return not any(keyword in mail.lower() for keyword in keywords)

def output(target):
    if target.n_domain:

        print_color('whois %s.'%target.n_domain, 2)

        # 当超时或者出现错误时，重试3次
        for i in range(1,4):
            try:
                data = get_whois(target.n_domain)['raw'][0]
                mails = findall(r'[\w\.-]+@[\w-]+\.[\w\.-]+', data)
                mails = filter(filter_mail, mails) if mails else None
                if mails:
                    target.mail = mails[0].lower()
                    break
            except:
                print_color('re-whois %s %d number of times' % (target.n_domain, i), 2)

        if hasattr(target,'mail'):
            print_color(target.mail, 1)

        print('')
