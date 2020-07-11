#
#  +--------------------+
#  | Single linked list |
#  +--------------------+
#
#  Author: Davi Villalva
#    Year: 2019
#
#  Even though I've known this data structure for ages, I decided
#  to write it in several languages for exercise.
#

# The Node class.
class Node(object):
    
    # Constructor.
    def __init__(self, value):

        # The value this Node holds.
        self.value = value
        
        # A link to the next Node.
        self._next = None

# The Single Linked List class.
class SingleLinkedList(object):
    
    # Constructor.
    def __init__(self, iterable=None):

        # The first Node of the List.
        self._first = None

        # The last Node of the List.
        self._last = None

        if iterable is not None:
            for value in iterable:
                self.insert(value)

    # Inserts a new value in the List.
    def insert(self, value):

        # Creating the new Node.
        node = Node(value)

        # If the new node is the first one,
        # simply sets as the first and the last.
        if self._first is None:
            self._first = node
            self._last = node

        # If it's not, then append it to the end
        else:
            self._last._next = node
            self._last = node

    def remove(self, value):

        # Search for the first ocurrence of the value
        # in the List.
        current = self._first
        prev = None
        found = None

        while current is not None:
            if current.value == value:
                found = current
                break

            prev = current
            current = current._next

        # If there is no node with the same value,
        # exit the function.
        if found is None:
            return

        # If there's no previous Node, then we set a new
        # first one.
        if prev is None:
            self._first = found._next

        # If there's, then we set the previous Node's next
        # as the found Node's next.
        else:
            prev._next = found._next

        # If this is the last Node, then we set the
        # last node to the previous one (if any)
        if found is self._last:
            self._last = prev
            

    # The iterator
    def __iter__(self):
        current = self._first

        while current is not None:
            yield current.value
            current = current._next

    def __str__(self):
        return f'SingleLinkedList({str(list(iter(self)))})'

    __repr__ = __str__
    
# Tests

d = SingleLinkedList([0, 1, 2, 3])

print(d)

d = SingleLinkedList()
d.insert(0)
d.insert(1)
d.insert(2)
d.insert(3)

print(d)

d = SingleLinkedList([12, 0, 1, 2, 3, 4, 5])
d.remove(4)
d.remove(5)
d.remove(12)

print(d)
