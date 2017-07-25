#!/usr/bin/env python
# Copyright (C) 2014:
#    Gabes Jean, naparuba@gmail.com

import threading
from kunai_test import *

from kunai.gossip import gossiper


class TestGossip(KunaiTest):
    def setUp(self):
        gossiper.init({}, threading.RLock(), '127.0.0.1', 6768, 'testing', 'super testing', 1, 'QQQQQQQQQQQQQQQQQQ', [], [], False, 'private', True)
    
    
    def test_gossip(self):
        pass


if __name__ == '__main__':
    unittest.main()
