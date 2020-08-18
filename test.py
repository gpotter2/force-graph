# Copyright (c) 2020 Gabriel Potter
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import sys
import math

from collections import deque

from hamiltonian.render import animate
from hamiltonian.manager import HubManager

import numpy as np

# Test handler

class TestHandler:
    def __init__(self, actions_list):
        self.f = 0
        self.manager = HubManager(self.callback)
        self.actions_list = deque(actions_list)
        self.manager.add_hub("main")
        self.manager.add_hub("main2")

    def callback(self, manager):
        self.f += 1
        if self.f % 20 == 1 and self.actions_list:
            action = self.actions_list.popleft()
            manager.add_point(*action)

def test():
    h = TestHandler([
        ("node1", "main"),
        ("node2", "main"),
        ("node3", "main"),
        ("node4", "main"),
        ("node5", "main"),
        ("node6", "main"),
        ("node7", "main"),
        ("node8", "main"),
        ("node9", "node1"),
        ("node10", "node1"),
        ("node11", "node1"),
        ("node12", "main2"),
        ("node13", "main2"),
        ("node14", "main2"),
        ("node15", "node13"),
        ("node16", "node13"),
        ("node17", "node13"),
        ("node18", "node16"),
    ])
    # Start thread
    h.manager.start()

test()
