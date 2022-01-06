* Potential advisor/consultant(s): Mike Stillman
* Goal: speed up the computation of determinants and minors over a polynomial ring, or even a sparse matrix over a field
* Current status: available!
* Macaulay2 skill level: beginner/intermediate, and C++ experience
* Mathematical experience: undergraduate
* Reason(s) to participate: Learn internals of M2, or you need or want faster determinants for your research

## Project Description

[Xianglong Ni](https://math.berkeley.edu/~xlni/) (math graduate student at Berkeley) has started doing this in top level Macaulay2.  Migrating the methods to the engine would produce a very useful speedup in many cases.  The package FastLinAlg is designed to do some of this as well.  This project, besides adding C++ determinant and minors code, might integrate this with that package, and/or create a new package.

Related issues: [#1899](https://github.com/Macaulay2/M2/issues/1899) , [#1705](https://github.com/Macaulay2/M2/issues/1705)

