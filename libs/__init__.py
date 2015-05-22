#!/usr/bin/env python
# -*- coding: utf-8 -*-
from core.common import argparse
from core.common import runtime
from core.engine import Pr0beScan
from core.common import print_color,print_logo

# cli parser
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--plugins', help='Custom plugins list.')
parser.add_argument('-l', '--list', action='store_true', default=False, help='Print plugins list.')
parser.add_argument('-u', '--url', type=str, help='Target url with http://.')
args = parser.parse_args()

# begin time
btime = runtime()
