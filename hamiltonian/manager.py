# Copyright (c) 2020 Gabriel Potter
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Nodes Managers
"""

import math
import numpy as np

from collections import defaultdict

from .render import animate

def _get_circle_locs(r, n, phi=0):
    """
    Get the List of n desired locations in the circle of radius r
    """
    tht = 2 * math.pi / n
    return [
        np.array((r * math.cos(phi + tht * i),
                  r * math.sin(phi + tht * i)))
        for i in range(n)
    ]


def _get_next_hub_pos(hubs):
    """
    Get the position of the center of the next hub based on existing one
    """
    nb = len(hubs.keys())
    return np.array((nb % 2, nb * 2))


class HubManager(object):
    """
    Order Nodes in hubs
    """
    def __init__(self, callback=None, radius=1.):
        self.objects = defaultdict(list)
        self.hubs = {}
        self.callback = callback
        self.radius = radius
        self.new_points = {}
        self.updated = True

    def render_callback(self, render):
        """
        Internal function called on each frame
        """
        if self.callback:
            self.callback(self)
        if not self.updated:
            # We only refresh the destination positions if necessary
            self.refresh_dests(render)
            self.updated = True

    def start(self, **kwargs):
        """
        Start animating
        """
        animate(self.render_callback, **kwargs)

    def get_rad_and_phi(self, layer):
        """
        Internal function to get the radius and angles of Nodes
        around another one.
        """
        rd = self.radius / (2 ** layer)
        phi = math.pi / 4 if ((1 + layer) % 2) else 0
        return rd, phi

    def add_hub(self, name, pos=None, **kwargs):
        """
        Add a standalone hub

        :param name: the hub's name
        :param pos: the hub's position
        """
        self.objects[name] = []
        if pos is None:
            pos = _get_next_hub_pos(self.hubs)
        self.hubs[name] = pos
        self.new_points[name] = (None, kwargs)
        self.updated = False

    def add_point(self, name, under, **kwargs):
        """
        Add a point linked to another one

        :param name: the point's name
        :param under: the parent's name
        """
        self.objects[name] = []
        self.objects[under].append(name)
        self.new_points[name] = (under, kwargs)
        self.updated = False

    def refresh_dests(self, render, cur=None, center=None, i=0):
        """
        Internal function used to recalculate all destinations
        """
        if cur is None:
            # Entry: iterate through hubs
            for hub, pos in self.hubs.items():
                if hub in self.new_points:
                    kwargs = self.new_points.pop(hub)[1]
                    render.add_node(hub, pos, **kwargs)
                self.refresh_dests(render, cur=hub, center=pos, i=0)
            return
        subs = self.objects[cur]
        if not subs:
            # Node has no child
            return
        rd, phi = self.get_rad_and_phi(i)
        poss = _get_circle_locs(rd, len(subs), phi)
        for i, name in enumerate(subs):
            pos = center + poss[i]
            # Check for new point
            if name in self.new_points:
                # Create point at desired location
                under, kwargs = self.new_points.pop(name)
                node = render.add_node(name, pos, **kwargs)
                if under:
                    # Link to upper point
                    render.add_link(render.get_node(under), node, **kwargs)
            else:
                # Update node destination
                node = render.get_node(name)
                node.set_destination(pos)
            if self.objects[name]:
                self.refresh_dests(render, cur=name, center=pos, i=i+1)

