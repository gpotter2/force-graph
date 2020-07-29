import sys
import math
from render import animate, Spring

import numpy as np


def get_desired_locations(render, n):
    """
    Get the List of n desired locations in the circle of radius r
    """
    tht = 2 * math.pi / n
    phi = 0
    return [phi + tht * i for i in range(n)]


def init(render):
    render.set_radius(0.2)
    bases = get_desired_locations(render, 3)
    print(bases)
    for i, theta in enumerate(bases):
        static_node = render.add_node(2 * i + 1, theta=theta, static=True)
        node = render.add_node(2 * (i + 1))
        render.add_force(static_node, node, Spring(500, 0))
        
    #n3 = render.add_node(3, link_to=n2)
    #render.link(n1, n3)

animate(init)
