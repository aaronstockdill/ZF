ZF
==

Description
-----------

This package defines several basic programming tools centered on ZF Set Theory. Features include Sets (obviously), Integers, Rationals, Finite Ordinals, Pairs, Lists, Characters, and Strings. Notably absent are Reals.


How to Use it
-------------

Download the folder, and copy it into your project. In the Python file you want to use it in, use `import ZF`. If you want only certain features, you can import specific sections. Be warned that many sections rely on other sections, for example `import ZF.Strings` will grab basically everything anyway, as strings need numbers, structures and sets.


Examples
--------

Numbers:

	>>> import ZF
	>>> five = ZF.Ordinal(5)
	>>> three = ZF.Ordinal(3)
	>>> fifteen = five * three
	>>> print(fifteen)
	15
	>>> fifteen
	{{{{{{}, <snip> }}}}}

Lists:

	>>> import ZF
	>>> zero = ZF.ZERO
	>>> one = ZF.succ(zero)
	>>> two = ZF.succ(one)
	>>> three = ZF.succ(two)
	>>> l = ZF.List(zero, one, two, three)
	>>> print(l)
	[0, 1, 2, 3]
	>>> l
	{{{}}, {{}, {{{{}}}, {{{{{{}}, {}}, {{{{{{}}, {}}, {{}}, {}}}}}, {{{{}}, {}}}}, {{}}}}}}

Strings:

	>>> import ZF
	>>> s = ZF.String("Hello")
	>>> print(s)
	Hello
	>>> s
	{{ <still running, probably> }}
	

Why?
----

I really have no good reason why. It's slow, impractical, and frankly not even very informative. But it sure was fun to play with. 
