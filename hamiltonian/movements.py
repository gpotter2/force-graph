# Copyright (c) 2020 Gabriel Potter
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Possible movements of a Node
"""

import math

def sinc(x):
    if x == 0:
        return 1
    return math.sin(x) / x

class SincMovement(object):
    """
    A movement that follows a sinc function that is stabilized
    """
    def __init__(self, posi, posd, K=0.2, K2=0.2):
        self.pos = posi
        self.dest = posd
        self.K = K
        self.K2 = K2
        self.i = 0  # frame number

    def next(self):
        self.i += self.K
        p = sinc(self.i * self.K) / (1 + self.i * self.K2)
        return self.pos * p + self.dest * (1 - p)
    __next__ = next
