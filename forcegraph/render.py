"""
Render
"""

import sys
import time

from collections import defaultdict

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from matplotlib.patches import Circle
from matplotlib.lines import Line2D

class Node(object):
    def __init__(self, index, name, posi, static):
        self.index = index
        self.name = name
        self.pos = posi
        self.static = static

    def next_pos(self):
        if self.static:
            return self.pos
        # XXX TODO FIXME
        return self.pos + np.random.rand(2) * 0.01

    def __repr__(self):
        return repr(self.pos)



class Render(object):
    def __init__(self, callback=None, T=0.2):
        self.nodes = {}
        self.lines = {}
        self.callback = callback
        # constants
        self.T = T
        # create plot
        self.fig = plt.figure()
        self.ax = self.fig.add_axes([0, 0, 1, 1], frameon=False)
        self.ax.set_ylim((0, 1))
        self.ax.set_xlim((0, 1))
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
        return len(self.nodes.values())

    def add_node(self, name, pos, static=False, c='k'):
        index = self.next_index
        node = Node(index, name, pos, static)
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
            np.array(matplotlib.colors.to_rgba(c), ndmin=2)
        ]))
        return node

    def nmlz(self, i, j):
        return tuple(sorted([i, j]))

    def get_node(self, name):
        for node in self.nodes.values():
            if node.name == name:
                return node

    def add_link(self, a, b, kwargs={}):
        id = self.nmlz(a.index, b.index)
        self.lines[id] = (a.index, b.index, kwargs)
        # Append line to canvas
        line2d = Line2D(a.pos, b.pos, **kwargs)
        self.lines2d[id] = line2d
        self.ax.add_line(line2d)

    def next_frame(self):
        new_values = {}
        # Get next nodes locations
        for i, node in self.nodes.items():
            self.nodes_ar[i,:] = self.nodes[i].pos = node.next_pos()
        # Re calculate lines
        for line in self.lines:
            x = [self.nodes_ar[line[0],0], self.nodes_ar[line[1],0]]
            y = [self.nodes_ar[line[0],1], self.nodes_ar[line[1],1]]
            self.lines[line] = (x, y, self.lines[line][2])
    
    def draw_frame(self, t=0):
        self.next_frame()
        # Re-draw points
        self.points.set_offsets(self.nodes_ar)
        # Re-draw lines
        for line, dat in self.lines.items():
            x, y, _ = dat
            self.lines2d[line].set_data(x, y)
        # Callback
        if self.callback:
            self.callback(self)
        #print(self.nodes_ar)

def animate(callback):
    render = Render(callback)
    
    ani = animation.FuncAnimation(
        render.fig,
        render.draw_frame,
        interval=1,
        blit=False
    )
    plt.show()
