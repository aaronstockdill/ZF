"""
File: ZF.Structures
Author: Aaron Stockdill

The goal of this module is not to be the most efficient representation, but
to be the most true to the underlying mathematics.

This file contains several useful, simple data structures.
"""

# A little messy to sort out importing for the package or the file.
try:
    from .Sets import *
except SystemError:
    from Sets import *
    

class Pair(Set):
    """ Create an ordered pair from Set.
    """

    def __init__(self, *items):
        if len(items) == 0:
            super().__init__()
            return
        elif len(items) == 1:
            a, = items
            b = a
        elif len(items) == 2:
            a, b = items
        else:
            raise ValueError("Pairs are made of 0, 1 or 2 items.")
        super().__init__(Set(a), Set(a, b))

    def __str__(self):
        """ Nicer pair representation.
        """
        try:
            first, second = self
            return "<{},{}>".format(first, second)
        except ValueError:
            try:
                first, = self
            except ValueError:
                return "<>"
            else:
                return "<{}>".format(first)

    def __iter__(self):
        """ Extract the pair elements.
        """
        if super().__len__() == 0:
            return
        try:
            a, b = sorted(super().__iter__(), key=len)
            assert(len(a) == 1)
            assert(len(b) == 2)
        except ValueError:
            # This pair is accidentally a singleton
            a, = super().__iter__()
            first, = a
            yield first
        else:
            first, = a
            i, j = b
            if i == first:
                second = j
            else:
                second = i
            yield first
            yield second


class List(Pair):
    """ Linked-list style lists based on the pair.
    """
    
    def __init__(self, *items):
        if len(items) == 0:
            super().__init__()
        elif len(items) == 1:
            a, = items
            super().__init__(a, a)
        else:
            i = len(items) - 1
            a = items[i]
            i -= 1
            tail = Pair(a)
            tail.__class__ = self.__class__
            while i > 0:
                tail = Pair(items[i], tail)
                tail.__class__ = self.__class__
                i -= 1
            super().__init__(items[0], tail)
    
    def __str__(self):
        """ Slightly more typical view of a list.
        """
        return "[{}]".format(", ".join(str(i) for i in self))

    def __iter__(self):
        """ Make sure the list can be iterated over.
        """
        if super().__len__() == 0:
            return
        try:
            current, next_link = super().__iter__()
        except ValueError:
            # Last singleton.
            current, = super().__iter__()
            yield current
        else:
            yield current
            for item in next_link:
                yield item
    
    def __len__(self):
        """ Make len return the length of the list.
        """
        l = super().__len__()
        if l == 0:
            return 0
        elif l == 1:
            return 1
        _, next = super().__iter__()
        return 1 + len(next)
    
    
    def __add__(a, b):
        """ List concatenation.
        """
        if super().__len__() == 0:
            return b
        try:
            a1, a2 = super().__iter__()
            tail = a2 + b
        except ValueError:
            a1, = super().__iter__()
            tail = b
        result = Pair(a1, tail)
        result.__class__ = a.__class__
        return result
        
        


def _test_structures():
    print(Pair())
    print(Pair('a', 'b'))
    print(Pair('a'))
    
    print(List())
    print(List('a'))
    print(List('a', 'b'), len(List('a', 'b')))
    print(List('a', 'b', 'c', 'd'))
    a = List('a', 'a', 'a', 'a')
    print(a, len(a), repr(a))
    print(a + List('b', 'b'))


if __name__ == "__main__":
    import cProfile
    cProfile.run("_test_structures()")
    # _test_structures()
