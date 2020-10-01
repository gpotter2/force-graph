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
from itertools import cycle, count

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
    def __init__(self, uuid, name, posi, text):
        self.uuid = uuid
        self.name = name
        self.pos = posi
        self.movement_cls = SincMovement
        self.movement = None
        self.text = text
        self.c = next(colors)

    def set_destination(self, pos):
        """
        Change the destination of the node.
        This also resets the current movement.
        """
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
        # Used to store the objects
        self.nodes = {}  # Dict[int, Node]
        # Used to store the objects index
        self.nodes_index_map = []  # List[int]
        self.lines = {}
        self.callback = callback
        self._counter = count()
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
    def next_uuid(self):
        """
        Internal property that gives the next node ID
        """
        return next(self._counter)

    def add_node(self, name, pos):
        """
        Add a Node to the graph.

        :param name: the node's name
        :param pos: the initial position of the Node
        """
        uuid = self.next_uuid
        # Annotate point
        text = self.ax.annotate(name, pos)
        # Create Node object
        node = Node(uuid, name, pos, text)
        if name in self.nodes:
            raise ValueError("Index name already present")
        # Save node
        self.nodes[uuid] = node
        self.nodes_index_map.append(uuid)
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

    def remove_node(self, name):
        """
        Remove a node, and all the links its in.

        :param name: the node's name
        """
        node = self.get_node(name)
        if node is None:
            raise ValueError("Unknown node !")
        # We get the index to remove the matching data
        index = self.nodes_index_map.index(node.uuid)
        del self.nodes_index_map[index]
        # Unregister the node from graphical data
        self.nodes_ar = np.delete(
            self.nodes_ar,
            index,
            axis=0
        )
        self.points.set_offsets(self.nodes_ar)
        self.points.set_facecolors(np.delete(
            self.points.get_facecolors(),
            index,
            axis=0
        ))
        self.ax.texts.remove(node.text)
        self.ax.stale = True
        # Remove all lines the node is in
        for line in self.lines.copy():
            if node.uuid in line:
                self.remove_link(line)
        # Remove node
        del self.nodes[node.uuid]

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
        """
        id = self.nmlz(a.uuid, b.uuid)
        self.lines[id] = id
        # Append line to canvas
        line2d = Line2D(a.pos, b.pos, c=a.c)
        self.lines2d[id] = line2d
        self.ax.add_line(line2d)

    def remove_link(self, tup):
        """
        Remove a line (link) between two nodes.
        
        :param tup: a tuple of nodes or of their UUIDs
        """
        if all(isinstance(x, Node) for x in tup):
            a, b = tup
            id = self.nmlz(a.uuid, b.uuid)
        else:
            id = self.nmlz(*tup)
        del self.lines[id]
        line2d = self.lines2d[id]
        del self.lines2d[id]
        self.ax.lines.remove(line2d)
        self.ax.stale = True

    def next_frame(self):
        """
        Internal function used to calculate the next frame.
        """
        new_values = {}
        uuids_index = {}
        # Get next nodes locations
        for i, uuid in enumerate(self.nodes_index_map):
            node = self.nodes[uuid]
            uuids_index[uuid] = i
            self.nodes_ar[i,:] = node.next_pos()
        # Re calculate lines
        for line in self.lines:
            i0, i1 = uuids_index[line[0]], uuids_index[line[1]]
            x = [self.nodes_ar[i0,0], self.nodes_ar[i1,0]]
            y = [self.nodes_ar[i0,1], self.nodes_ar[i1,1]]
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
