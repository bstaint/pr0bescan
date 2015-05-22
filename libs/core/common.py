#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import time
import argparse
import logging
from libs.colorama import init
from libs.colorama import Fore, Back, Style

Program = 'Pro0beScan'
Version = 'Beta 4.0'
Author = 'bstaint'
Blog = 'http://www.bstaint.net/'


def print_logo():
    print(Fore.YELLOW + '''
 ______     _____ _          _____                 
 | ___ \   |  _  | |        /  ___|                
 | |_/ / __| |/' | |__   ___\ `--.  ___ __ _ _ __  
 |  __/ '__|  /| | '_ \ / _ \`--. \/ __/ _` | '_ \ 
 | |  | |  \ |_/ / |_) |  __/\__/ / (_| (_| | | | |
 \_|  |_|   \___/|_.__/ \___\____/ \___\__,_|_| |_|
                                %s %s''' % (Program, Version))
    print(Fore.RED + '[!] Usage of %s Damage other Computer!!!\n' % Program+Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_color(msg, mark = 0, record = False):
    if mark == 0:
        msg = Fore.RED + '[-] %s' % msg
    elif mark == 1:
        msg = Fore.GREEN + '[+] %s' % msg
    elif mark == 2:
        msg = Fore.YELLOW + '[*] %s' % msg

    sys.stdout.write(msg + Fore.RESET + Back.RESET + Style.RESET_ALL + '\n')

def runtime():
    return time.time()

def query_yes_no(question, default="no"):
    valid = {"y":True,"n":False}

    while True:
        sys.stdout.write(Fore.YELLOW + question + ' [y/N] ' + Fore.RESET + Back.RESET + Style.RESET_ALL)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write(Fore.YELLOW + "please respond with 'y' or 'n'.\n" + Fore.RESET + Back.RESET + Style.RESET_ALL)

init()

# 记录日志
logging.basicConfig(filename = os.path.join(os.getcwd()+'/output', 'debug.log'), level = logging.DEBUG)
