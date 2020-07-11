#
#  +----------------------------+
#  | Simple tree implementation |
#  +----------------------------+
#
#  Author: Davi Villalva
#    Year: 2019
#
#  Even though I've known this data structure for ages, I decided
#  to write it in several languages for exercise.
#

import sys

# The Tree Node class.
class Node(object):

    # Constructor.
    def __init__(self, value=None):
        
        # The value this Node holds.
        self.value = value

        # The Node's parent.
        self._parent = None

        # The Node's children.
        self._children = []
    
    # Releases the Node from any relationship.
    def detach(self):
        if self._parent is not None:
            self._parent._children.remove(self)

        for child in self._children:
            child._parent = None
    
    # Adds a child to this Node.
    def add_child(self, child):
        child.detach()

        child._parent = self
        self._children.append(child)
    
    # Prints recursively
    def print(self, ident=0):
        sys.stdout.write("   " * ident)
        sys.stdout.write(f"{self.value}")
        sys.stdout.write("\n" if len(self._children) == 0 else ":\n")

        for child in self._children:
            child.print(ident + 1)

# Tests

root = Node("root")
root.add_child(Node("item 0"))
root.add_child(Node("item 1"))
root.add_child(Node("item 2"))

item_3 = Node("item 3")
item_3.add_child(Node("sub_item 0"))
item_3.add_child(Node("sub_item 1"))
item_3.add_child(Node("sub_item 2"))
root.add_child(item_3)

root.add_child(Node("item 4"))

root.print()
