# Copyright (c) 2020 Gabriel Potter
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

import sys
import math

from hamiltonian.render import animate

import numpy as np


def get_desired_locations(render, n):
    """
    Get the List of n desired locations in the circle of radius r
    """
    tht = 2 * math.pi / n
    phi = 0
    return [phi + tht * i for i in range(n)]


def init(render):
    bases = get_desired_locations(render, 3)
    for i, theta in enumerate(bases):
        static_node = render.add_node(2 * i + 1, theta=theta, static=True)
        node = render.add_node(2 * (i + 1))
        
    #n3 = render.add_node(3, link_to=n2)
    #render.link(n1, n3)

i = 0

def callback(render):
    global i
    pos = np.random.rand(2)
    render.add_node("point%s" % i, pos)
    a = render.get_node("point%s" % i)
    b = render.get_node("point%s" % (i - 1))
    if a and b:
        render.add_link(a, b)
    i += 1

animate(callback)
