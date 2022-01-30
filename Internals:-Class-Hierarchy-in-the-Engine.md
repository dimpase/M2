Work in progress. Contributors: Michael Burr, Anton Leykin, (your-name-here)

## Rings

In order to see some of the inheritance of types, run `showStructure` in M2.  There may be further inheritance that is not shown.  In addition, running this within debug Core will give additional structure information.  To find out information about a specific ring, run `<Ring name>.RawRing` within debug Core.

Within the d-language, `RawRing` is a pointer to the struct of a ring.  Within the code, sometimes `RawRingOrNull` is used, often for debugging purposes.  `RawRingOrNull` allows for a null pointer for a nonexistent ring.  Since exceptions can't be used between C and C++, this gives a way for error handling.  For example, the function `toExper(x:RawRing):Expr` produces a ring while `toExper(x:RawRingOrNull):Expr` produces a ring or an error message.  To find the `toExpr` options, see `util.d`.

For the C/C++ code, the file `e/x-relem.cpp` contains Ring Elements and Rings.  The file `e/ring.hpp` has the class for `Ring`.  Here, Rings are mutable engine objects.  The way this has been coded, when converting between ring types, a cast must be used, so if a new ring type is added, the conversion has to be added to the `Ring` class directly.