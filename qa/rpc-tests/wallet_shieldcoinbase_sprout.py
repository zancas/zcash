#!/usr/bin/env python3

import inspect
import os

# To keep pyflakes happy
WalletShieldCoinbaseTest = object

cwd = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
exec(compile(open(os.path.join(cwd, 'wallet_shieldcoinbase.py')).read(), os.path.join(cwd, 'wallet_shieldcoinbase.py'), 'exec'))

class WalletShieldCoinbaseSprout(WalletShieldCoinbaseTest):
    def __init__(self):
        super(WalletShieldCoinbaseSprout, self).__init__('sprout')

if __name__ == '__main__':
    WalletShieldCoinbaseSprout().main()
