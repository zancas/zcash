#!/usr/bin/env python3

import inspect
import os

# To keep pyflakes happy
WalletShieldCoinbaseTest = object

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
exec(compile(open(os.path.join(cwd, 'wallet_shieldcoinbase.py')).read(), os.path.join(cwd, 'wallet_shieldcoinbase.py'), 'exec'))

class WalletShieldCoinbaseSapling(WalletShieldCoinbaseTest):
    def __init__(self):
        super(WalletShieldCoinbaseSapling, self).__init__('sapling')

if __name__ == '__main__':
    WalletShieldCoinbaseSapling().main()
