#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs import *
from plugins import *

def main():
    target = Pr0beScan()

    if args.list:
        [print_color(p,1) for p in plugins]

    elif args.url:
        print_logo()
        print_color('init scaning', 2)

        if not target.probe(args.url):
            print_color('init probe faild!')
            exit(-1)

        target.print_info()

        pls = ['plugins.%s' % s for s in args.plugins.split(',')] if args.plugins else plugins
        [target.plugin(p) for p in pls]

        print_color('end time %1.f secs'%(runtime()-btime), 2)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
