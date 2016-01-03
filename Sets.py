"""
File: ZF.Sets
Author: Aaron Stockdill

The goal of this module is not to be the most efficient representation, but
to be the most true to the underlying mathematics.

This file contains the implementation of the Set, and some surrounding useful
functions.
"""


def powerset(original):
    """ Return the powerset of the original set.
    """
    if '_powerset' in dir(original):
        return original._powerset()
    raise TypeError("Must be given a Set, or subclass thereof.")

P = powerset # Useful alias


def union(a, b):
    """ Return the union of a and b.
    """
    return Set(a, b).union()

def intersection(a, b):
    """ Return the intersection of a and b.
    """
    return Set(a, b).intersection()


class Set(object):
    """ The primitive Set class.
    """

    def __init__(self, *items):
        """ Create the set.
        """
        self.items = frozenset(items)

    def __hash__(self):
        """ Required for Python 'set' hashing.
        """
        return hash(self.items)

    def __repr__(self):
        """ How the set is internally represented.
        """
        if len(self.items) == 0:
            return "{}"
        return "{" + ", ".join(repr(i) for i in self.items) + "}"

    def __str__(self):
        """ A prettier view of the set for printing.
        """
        if len(self.items) == 0:
            return "∅"
        return "{" + ", ".join(str(i) for i in self.items) + "}"

    def __contains__(self, something):
        """ Return whether the set contains something.
        """
        return something in self.items

    def __len__(self):
        """ Return the size of the set (number of elements).
        """
        return len(self.items)

    def __lt__(self, other):
        """ Set ordering is impossible.
        """
        raise TypeError("Sets are not orderable.")
    def __le__(self, other):
        raise TypeError("Sets are not orderable.")
    def __gt__(self, other):
        raise TypeError("Sets are not orderable.")
    def __ge__(self, other):
        raise TypeError("Sets are not orderable.")

    def __eq__(self, other):
        """ Sets are equal iff they have the same elements.
        """
        if not isinstance(other, Set):
            return False
        return (self.subset(other, strict=False)
            and other.subset(self, strict=False))

    def __bool__(self):
        """ Python Truthiness, based on whether it is the empty set.
        """
        return not self.empty()

    def __iter__(self):
        """ Iterate through all the items.
        """
        for i in self.items:
            yield i

    def _powerset(self):
        """ Generate the powerset of self.
        """
        if self.empty():
            return Set(Set())
        else:
            item = self.take()
            new_set = self.delete(Set(item))
            sub_powerset = new_set._powerset()
            result = sub_powerset.items.union({
                Set(a, Set(item)).union() for a in sub_powerset
            })
            return Set(*result)


    def delete(self, other_set):
        """ Return a set with all the same elements as self,
            except those in other_set.
        """
        return Set(*self.items.difference(other_set.items))

    def empty(self):
        """ Return whether the set is empty.
        """
        return len(self.items) == 0

    def union(self):
        """ Return the set union.
        """
        all_items = set()
        for subset in self.items:
            for item in subset:
                all_items.add(item)
        return Set(*all_items)

    def intersection(self):
        """ Return the set intersection.
        """
        intersection = set()
        union = self.union()
        for item in union:
            add = True
            for subset in self.items:
                add = add and (item in subset)
            if add:
                intersection.add(item)
        return Set(*intersection)

    def subset(self, other, strict=False):
        """ Return whether this is a subset of other.
            If the strict flag is set, make sure they are not equal.
        """
        result = self.items.issubset(other.items)
        if not strict:
            return result
        else:
            return result and not (self == other)

    def superset(self, other, strict=False):
        """ Determine whether self is a superset of other.
            If the strict flag is set, make sure they are not equal.
        """
        return other.subset(self, strict)

    def take(self, number=1):
        """ Take random elements from the set, up to number of them.
        """
        result = set()
        for i, item in enumerate(self):
            if i < number:
                result.add(item)
        if not result:
            return None
        if number == 1:
            return list(result)[0]
        return result


def _test_sets():
    print(Set())
    un = Set(Set(), Set(Set()))
    print(un)
    print(un.delete(Set(Set())))
    print(powerset(un))
    print(un.union())
    a = Set('a', 'b', 'c')
    b = Set('c', 'd', 'e')
    print(a, b, intersection(a, b))


if __name__ == "__main__":
    import cProfile
    cProfile.run("_test_sets()")
    # _test_sets()
