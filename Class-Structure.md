Work in progress. Contributors: Michael Burr, (your-name-here)

## Rings

showStructure shows the structure (all the types).  debug Core {Ring}.RawRing has info about a ring.  RawRing is a pointer to a struct of a Ring.  RawRingOrNull null is 0 identifier.  Allows a null ring (often used for debugging).  We can't use exceptions between C and C++, so this is a way for error handling.  x-relem.cpp has ring elements and rings.  Internally, passing a pointer (which may be null).  Code checks for null or other features and either produces an error (try-catch) and provides object.  toExper(x:RawRing):Expr produces a ring, toExper(x:RawRingOrNull):Expr produces a ring or an error message.  util.d has all of the toExpr's.  ring.hpp in e has the class for the ring.  Rings are mutable engine objects.  Types of rings are casts, so you have to add a new ring type in the class directly.

## Doxygen

It isn't complete, but it has some useful information.  Especially the class structure and inheritance.

## Branches

Differences between different branches of M2 include garbage collection.

## Unit tests

"ctest -R unit" does the tests labeled unit.  Alternately, gmake check (different format).  These are fast tests to check easy things.