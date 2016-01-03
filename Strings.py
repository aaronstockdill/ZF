"""
File: ZF.Strings
Author: Aaron Stockdill

The goal of this module is not to be the most efficient representation, but
to be the most true to the underlying mathematics.

Basic string support is provided by this file.
"""

# A little messy to sort out importing for the package or the file.
try:
    from .Sets import *
    from .Numbers import *
    from .Structures import *
except SystemError:
    from Sets import *
    from Numbers import *
    from Structures import *


class Character(Ordinal):
    """ A character is just an ordinal that has a clever representation.
    """

    def __init__(self, char=None):
        if char is None:
            super().__init__()
        elif isinstance(char, str):
            if len(char) != 1:
                raise ValueError("Character must be a single letter.")
            super().__init__(ord(char))
        elif isinstance(char, int):
            super().__init__(char)

    def __str__(self):
        return chr(int(super().__str__()))


class String(List):
    """ A string is a list of Characters.
    """

    def __init__(self, string):
        super().__init__(*[Character(s) for s in string])

    def __str__(self):
        return "".join(str(s) for s in self)


def _test_strings():
    print(succ(Character('a')))
    s = String('Hello, I am a set.')
    print(s)
    print(String("Se") + String("ts"))


if __name__ == "__main__":
    import cProfile
    cProfile.run("_test_strings()")
    # _test_strings()
