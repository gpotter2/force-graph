"""
Test & demo file
"""

from collections import deque
from enum import Enum

import numpy as np
from hamiltonian.manager import Manager

class TestManager(Manager):
    """
    A hectic test to show that the point generation,
    line generation, point deletion, line deletion,
    point movements work.

    :param per: frames between two cycles of actions
    """
    def __init__(self, per):
        super(TestManager, self).__init__(
            callback=lambda x: x.refresh()
        )
        self.ind = 0
        self.per = per
        self.prevs = []

    def update(self, render):
        self.ind += 1
        cyl = self.ind // self.per
        action = self.ind % self.per
        if action == 0:
            node = render.add_node(
                "node%i" % cyl,
                np.random.rand(2)
            )
            self.prevs.append(node)
        elif action == 1 and cyl > 1:
            a, b = self.prevs[-1], self.prevs[-2]
            render.add_link(a, b)
        elif action == 2 and cyl > 1:
            self.prevs[-1].set_destination(
                np.random.rand(2)
            )
        elif action == 3 and cyl > 5:
            render.remove_node(self.prevs[0].name)
            del self.prevs[0]

TestManager(20).start()
