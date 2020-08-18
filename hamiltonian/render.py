# Copyright (c) 2020 Gabriel Potter
# This work is licensed under the terms of the MIT license.
# For a copy, see <https://opensource.org/licenses/MIT>.

"""
Rendering engine.

Capabilities:
    - display dynamic nodes
    - display dynamic links
    - display nodes names
"""

import sys
import time

from collections import defaultdict
from itertools import cycle

from .movements import SincMovement

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.patches import Circle
from matplotlib.lines import Line2D

colors = cycle("bgrcmyk")

class Node(object):
    """
    A Node object.
    """
    def __init__(self, index, name, posi, text):
        self.index = index
        self.name = name
        self.pos = posi
        self.movement_cls = SincMovement
        self.movement = None
        self.text = text
        self.c = next(colors)

    def set_destination(self, pos):
        self.movement = self.movement_cls(self.pos, pos)
    
    def next_pos(self):
        """
        Returns the next position of the node
        """
        if self.movement is None:  # Static
            pos = self.pos
        else:
            pos = next(self.movement)
        self.pos = pos
        self.text.set_position(pos)
        return pos

    def __repr__(self):
        return repr(self.pos)



class Render(object):
    """
    Rendering engine.

    Please use animate() instead of calling it directly.
    """
    def __init__(self, callback=None):
        self.nodes = {}
        self.lines = {}
        self.callback = callback
        # create plot
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1], frameon=False)
        self.points = None
        self.lines2d = {}
        # radius mode
        self.center = np.array((0.5, 0.5))
        # Init matplotlib structs
        self.nodes_ar = np.zeros((0, 2))
        self.points = self.ax.scatter(self.nodes_ar[:,0],
                                      self.nodes_ar[:,1],
                                      s=50)

    @property
    def next_index(self):
        """
        Internal property that gives the next node ID
        """
        return len(self.nodes.values())

    def add_node(self, name, pos):
        """
        Add a Node to the graph.

        :param name: the node's name
        :param pos: the initial position of the Node
        :param movement: the movement to follow. If None, static
        :param c: the color of the Node given to matplotlib
        """
        index = self.next_index
        text = self.ax.annotate(name, pos)
        node = Node(index, name, pos, text)
        if name in self.nodes:
            raise ValueError("Index name already present")
        self.nodes[index] = node
        # Append point to scatter
        self.nodes_ar = np.concatenate([
            self.nodes_ar,
            np.array(pos, ndmin=2)
        ])
        self.points.set_offsets(self.nodes_ar)
        self.points.set_facecolors(np.concatenate([
            self.points.get_facecolors(),
            np.array(matplotlib.colors.to_rgba(node.c), ndmin=2)
        ]))
        return node

    def nmlz(self, i, j):
        """
        Internal function used to normalize the ID of a link
        """
        return tuple(sorted([i, j]))

    def get_node(self, name):
        """
        Get a Node object based on its name.

        :param name: the Node name
        """
        for node in self.nodes.values():
            if node.name == name:
                return node

    def add_link(self, a, b):
        """
        Add a line (link) between two nodes.

        :param a:
        :param b: a Node object (acquired using .get_node())
        :param kwargs: extra matplotlib arguments
        """
        id = self.nmlz(a.index, b.index)
        self.lines[id] = (a.index, b.index)
        # Append line to canvas
        line2d = Line2D(a.pos, b.pos, c=a.c)
        self.lines2d[id] = line2d
        self.ax.add_line(line2d)

    def next_frame(self):
        """
        Internal function used to calculate the next frame.
        """
        new_values = {}
        # Get next nodes locations
        for i, node in self.nodes.items():
            self.nodes_ar[i,:] = node.next_pos()
        # Re calculate lines
        for line in self.lines:
            x = [self.nodes_ar[line[0],0], self.nodes_ar[line[1],0]]
            y = [self.nodes_ar[line[0],1], self.nodes_ar[line[1],1]]
            self.lines[line] = (x, y)
    
    def draw_frame(self, t=0):
        """
        Internal function used to draw a frame.
        """
        self.next_frame()
        # Re-draw points
        self.points.set_offsets(self.nodes_ar)
        # Re-draw lines
        for line, dat in self.lines.items():
            x, y = dat
            self.lines2d[line].set_data(x, y)
        # Callback
        if self.callback:
            self.callback(self)
        # Auto rescale
        self.ax.relim()
        self.ax.autoscale_view()

def animate(callback, interval=1, output=None):
    """
    Start an animation

    :param callback: a callback called on each frame with the renderer
        as argument
    :param output: an output to write the animation instead of showing it
    """
    render = Render(callback)
    
    ani = animation.FuncAnimation(
        render.fig,
        render.draw_frame,
        interval=interval,
        blit=False
    )
    if output:
        # Save to gif file
        ani.save(output, writer='imagemagick', fps=30)
    else:
        # Show
        plt.show()
