#!/usr/bin/env python

from __future__ import print_function
import sys
import re

USAGE = 'usage: check_untested_methods.py <rootdir>'
try:
  rootdir = sys.argv[1]
except:
  print(USAGE)
  sys.exit(1)

sys.path.insert(0, f'{rootdir}/utils/python-rpc')

from framework import daemon
from framework import wallet

modules = [
    {
        'name': 'daemon',
        'object': daemon.Daemon(),
        'path': f'{rootdir}/src/rpc/core_rpc_server.h',
        'ignore': [],
    },
    {
        'name': 'wallet',
        'object': wallet.Wallet(),
        'path': f'{rootdir}/src/wallet/wallet_rpc_server.h',
        'ignore': [],
    },
]

error = False
for module in modules:
  for line in open(module['path']):
    if 'MAP_URI_AUTO_JON2' in line or 'MAP_JON_RPC' in line:
      match = re.search('.*\"(.*)\".*', line)
      name = match[1]
      if name in module['ignore'] or name.endswith('.bin'):
        continue
      if 'MAP_URI_AUTO_JON2' in line:
        if not name.startswith('/'):
          print(f'Error: {name} does not start with /')
          error = True
        name = name[1:]
      if not hasattr(module['object'], name):
        print(
            f"Error: {module['name']} API method {name} does not have a matching function"
        )
        error = True

sys.exit(1 if error else 0)
