"""
File: ZF.Numbers
Author: Aaron Stockdill

The goal of this module is not to be the most efficient representation, but
to be the most true to the underlying mathematics.

This file contains natural numbers, integers and rational numbers. The natural
numbers are called Ordinals as they are based on the theory of Ordinals, but
lack limit ordinals.
"""

# A little messy to sort out importing for the package or the file.
try:
    from .Sets import *
    from .Structures import *
except SystemError:
    from Sets import *
    from Structures import *


def succ(ordinal):
    """ Successor of the ordinal
    """
    if '_succ' in dir(ordinal):
        return ordinal._succ()
    else:
        raise TypeError("Must be given an Ordinal.")


def pred(ordinal):
    """ Predecessor of the ordinal.
    """
    if '_pred' in dir(ordinal):
        return ordinal._pred()
    else:
        raise TypeError("Must be given an Ordinal.")


class Ordinal(Set):
    """ An ordinal from ZF Set theory """

    def __init__(self, from_number=0):
        """ Initialize the ordinal.
        """
        super().__init__()
        if isinstance(from_number, int):
            if from_number > 0:
                new = Ordinal(0)
                for _ in range(from_number):
                    new = succ(new)
                self.items = new.items
            if from_number < 0:
                raise ValueError("Ordinals can only be "
                                 "created from positive ints.")
        elif isinstance(from_number, Integer):
            sign, value = from_number
            assert(sign == Integer.POSITIVE or value == ZERO)
            self.items = value.items
        elif isinstance(from_number, Set):
            self.items = from_number.items

    @classmethod
    def from_iter(cls, structure):
        """ Create a new ordinal from the set structure.
        """
        new = cls()
        new.items = structure
        return new

    def __lt__(self, other):
        """ Less than.
        """
        return self in other

    def __le__(self, other):
        return self == other or self < other
    def __gt__(self, other):
        return not (self <= other)
    def __ge__(self, other):
        return self == other or self > other

    def __str__(self):
        """ A nice base-10 representation of the Ordinal.
        """
        number = 0
        new = self
        while new != ZERO:
            new = pred(new)
            number += 1
        return str(number)

    def __add__(a, b):
        """ Add together two ordinals.
        """
        if b == ZERO:
            return a
        else:
            z = pred(b)
            return succ(a + z)

    def __sub__(a, b):
        """ Subtract b from a.
        """
        if b == ZERO:
            return a
        else:
            z = pred(b)
            return pred(a - z)

    def __mul__(a, b):
        """ Multiply two ordinals.
        """
        if b == ZERO:
            return ZERO
        else:
            z = pred(b)
            return (a*z) + a

    def __truediv__(a, b):
        """ Divide a by b.
        """
        if b == ZERO:
            raise ZeroDivisionError
        q = ZERO
        r = a
        while r >= b:
            q = succ(q)
            r = r - b
        if r == ZERO:
            return q
        else:
            return Rational(a, b)

    def __mod__(a, b):
        if b == ZERO:
            raise ZeroDivisionError
        r = a
        while r >= b:
            r = r - b
        return r

    def _succ(self):
        """ The successor of the Ordinal.
        """
        new = Set(
            Set(self),
            self
        ).union()
        new.__class__ = self.__class__
        return new

    def _pred(self):
        """ The predecessor of the Ordinal.
        """
        if self == ZERO:
            raise ValueError("Zero has no predecessor.")
        return Ordinal(self.union())

    def inverse(self):
        return Rational(succ(ZERO), self)


class Integer(Pair):
    """ Represent Integers as a pair of sign and ordinal.
    """

    # These are a bit convoluted, but they had to not accidently reduce to
    # a singleton when used with an ordinal.
    POSITIVE = Set(Set(Set(Set())), Set(Set()))
    NEGATIVE = Set(Set(Set(Set(Set()))), Set(Set()))

    def __init__(self, value=0):
        """ Initialize the Integer, possibly from an int value.
        """
        sign = Integer.POSITIVE
        if isinstance(value, Ordinal):
            number = value
        elif isinstance(value, Integer):
            sign, number = value
        elif isinstance(value, Pair):
            sign, number = value
            assert(sign == Integer.POSITIVE or sign == Integer.NEGATIVE)
            assert(isinstance(number, Ordinal))
        else:
            number = Ordinal(abs(value))
            if value < 0:
                sign = Integer.NEGATIVE
        super().__init__(sign, number)

    def __str__(self):
        """ Slightly more typical display.
        """
        sign, number = self
        output = str(number)
        if sign == Integer.NEGATIVE and number != ZERO:
            output = "-" + output
        return output

    def __lt__(self, other):
        """ Less than.
        """
        self_sign, self_val = self
        other_sign, other_val = other
        if self_sign == other_sign == Integer.POSITIVE:
            return self_val < other_val
        elif self_sign == other_sign == Integer.NEGATIVE:
            return other_val < self_val
        elif self_sign == Integer.POSITIVE:
            return False
        else:
            return True

    def __le__(self, other):
        return self == other or self < other
    def __gt__(self, other):
        return not (self <= other)
    def __ge__(self, other):
        return self == other or self > other

    def __add__(a, b):
        signa, vala = a
        signb, valb = b
        if signa == signb == Integer.POSITIVE:
            pair = Pair(Integer.POSITIVE, vala + valb)
            pair.__class__ = self.__class__
            return pair
        elif signa == signb == Integer.NEGATIVE:
            return Integer(Pair(Integer.NEGATIVE, vala + valb))
        elif signa == Integer.POSITIVE and signb == Integer.NEGATIVE:
            if valb >= vala:
                sign = Integer.NEGATIVE
                value = valb - vala
            else:
                sign = Integer.POSITIVE
                value = vala - valb
            return Integer(Pair(sign, value))
        else:
            if vala >= valb:
                sign = Integer.NEGATIVE
                value = vala - valb
            else:
                sign = Integer.POSITIVE
                value = valb - vala
            return Integer(Pair(sign, value))

    def __sub__(a, b):
        return a + b.negative()

    def __mul__(a, b):
        signa, vala = a
        signb, valb = b
        if signa == signb:
            sign = Integer.POSITIVE
        else:
            sign = Integer.NEGATIVE
        return Integer(Pair(sign, vala * valb))

    def __truediv__(a, b):
        signa, vala = a
        signb, valb = b
        if signa == signb:
            sign = Integer.POSITIVE
        else:
            sign = Integer.NEGATIVE
        number = vala / valb
        if isinstance(number, Rational):
            num, denom = number
            if sign == Integer.NEGATIVE:
                return Rational(num.negative(), denom)
            else:
                return number
        else:
            return Integer(Pair(sign, number))

    def __mod__(a, b):
        b_sign, b_val = Integer(b)
        if b_sign == Integer.NEGATIVE:
            raise ValueError("Cannot mod by a negative number.")
        else:
            sign, value = a
            if sign == Integer.NEGATIVE:
                return Integer(b - Integer(value % b_val))
            else:
                return Integer(value % b_val)

    def inverse(self):
        """ Return the inverse of the integer (the reciprocal).
        """
        sign, val = self
        num = Integer(Pair(sign, succ(ZERO)))
        return Rational(num, val)

    def negative(self):
        """ Return the negative of the integer.
        """
        sign, value = self
        new_sign = Integer.NEGATIVE
        if sign == Integer.NEGATIVE or value == ZERO:
            new_sign = Integer.POSITIVE
        return Integer(Pair(new_sign, value))

    def is_negative(self):
        """ Returns whether the integer is negative.
        """
        sign, val = self
        if sign == Integer.NEGATIVE and val != 0:
            return True
        return False


class Rational(Pair):
    """ A quotient class, based on ordered pairs.
    """

    def __init__(self, numerator, denominator):
        """ Numerator and denominator must be able to be Integers.
        """
        numerator = Integer(numerator)
        denominator = Integer(denominator)
        gcd = self._gcd(numerator, denominator)
        a = numerator / gcd
        b = denominator / gcd
        if b == succ(ZERO):
            self.__class__ = Integer
            self.__init__(a)
        else:
            super().__init__(a, b)

    def __str__(self):
        a, b = self
        return str(a) + "/" + str(b)

    def __add__(a, b):
        numa, dena = a
        numb, denb = b
        new_num = (numa * denb) + (numb * dena)
        new_denom = dena * denb
        return Rational(new_num, new_denom)

    def __sub__(a, b):
        numa, dena = a
        numb, denb = b
        new_num = (numa * denb) - (numb * dena)
        new_denom = dena * denb
        return Rational(new_num, new_denom)

    def __mul__(a, b):
        numa, dena = a
        numb, denb = b
        new_num = numa * numb
        new_denom = dena * denb
        return Rational(new_num, new_denom)

    def __truediv__(a, b):
        return a * b.inverse()

    def _gcd(self, a, b):
        """ Calculate the greatest common divisor of two Ordinals.
        """
        if b == Integer(ZERO) or b == ZERO:
            return a
        else:
            r = a % b
            return self._gcd(b, r)

    def inverse(self):
        """ Return the multiplicative inverse (i.e. the reciprocal)
            of the quotient.
        """
        a, b = self
        return Rational(b, a)

    def negative(self):
        """ Return the negative of the integer.
        """
        num, denom = self
        return Rational(num.negative(), denom)

    def is_negative(self):
        """ Returns whether the integer is negative.
        """
        num, _ = self
        return num.is_negative()


ZERO = Ordinal()


def _test_ord():
    x = Ordinal(2)
    print('    x =', x)
    print('x - 1 =', pred(x))
    print('x + 1 =', succ(x))

    y = Ordinal(6)
    print('    y =', y)

    print('x + y =', x + y)
    print('y - x =', y - x)
    print('x * y =', x * y)
    print('y / x =', y / x)

    nine = Ordinal(9)

    six = Ordinal(6)

    ans = nine / six
    print("9 / 6 =", ans)

    neg_four = Integer(-4)
    three = Integer(3)

    print("-4 + 3 =", neg_four + three)
    print("-4 * 3 =", neg_four * three)
    print("3 / -4 =", three / neg_four)
    print("-7 % 3 =", Integer(-7) % three)

    print("13 =", repr(Ordinal(13)))


if __name__ == "__main__":
    import cProfile
    # cProfile.run("_test_ord()")
    _test_ord()
