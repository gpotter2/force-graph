import sys
import math
from render import animate, Spring

def get_median_radius(r, n):
    # Circle: radius r
    # n points
    theta = 2 * math.pi / n
    # Alkashi
    # c**2 = a**2 + b**2 - 2*a*b*cos(C)
    return math.sqrt(2 * r ** 2 - 2 * r ** 2 * math.cos(theta))


def init(render):
    n1 = render.add_node(1)
    n2 = render.add_node(2)
    n3 = render.add_node(3)
    n4 = render.add_node(4)
    l = get_median_radius(render.l0, 3)
    print(render.l0)
    print(l)
    render.add_force(n1, n2, Spring(2000, l))
    render.add_force(n2, n3, Spring(2000, l))
    render.add_force(n3, n4, Spring(2000, l))
    #n3 = render.add_node(3, link_to=n2)
    #render.link(n1, n3)

animate(init)
