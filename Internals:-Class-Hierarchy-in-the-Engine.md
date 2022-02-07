Work in progress. Contributors: Michael Burr, Anton Leykin, (your-name-here)

## Rings

In order to see some of the inheritance of types, run `showStructure` in M2.  There may be further inheritance that is not shown.  Running this after typing `debug Core` (exposed Core unexported symbols) will give additional structure information.  To find out information about a specific ring, run `<Ring name>.RawRing` within `debug Core`.

Within the d-language, `RawRing` is a pointer to the struct of a ring.  Within the code, sometimes `RawRingOrNull` is used, often for debugging purposes.  `RawRingOrNull` allows for a null pointer for a nonexistent ring.  Since exceptions can't be used between C and C++, this gives a way for error handling.  For example, the function `toExpr(x:RawRing):Expr` produces a ring while `toExper(x:RawRingOrNull):Expr` produces a ring or an error message.  To find the `toExpr` options, see `util.d`.

For the C/C++ code, the file `e/x-relem.cpp` contains Ring Elements and Rings.  The file `e/ring.hpp` has the class for `Ring`.  Here, Rings are mutable engine objects.  The way this has been coded, when converting between ring types, a cast must be used, so if a new ring type is added, the conversion has to be added to the `Ring` class directly.

## Linear algebra in the M2 engine

The following are the notes used by Mike Stillman in the M2internals workshop on 3 Feb 2022.

```
mat.hpp
  MutableMatrix: abstract.
    rank, eigenvalues: member functions.
    
mutablemat-defs.hpp
  MutableMat<MT> : MutableMatrix    
  MT is "MatrixType"
    DMat<RT>  
      DMat<ARingZZpFlint>
      DMat<ARingGFFlint> ... all are managed matrices via flint.
    SMat<RT>
  RT is "RingType" "ARing's": ZZ, QQ, ZZ/p, GF, RR, CC
    ARingZZpFlint
    ARingZZpFFPACK (internal only)
    ARingGFFlint
    ARingGFFlintBig
    ARingZZ (GMP and soon: Flint)
    ARingQQ (GMP and soon: Flint)
    ARingRR
    ARingCC
    ARingRRR
    ARingCCC
    (ARingRRi)

mutablemat-imp.hpp
  MatrixOps::rank(mat)
  MatrixOps::eigenvalues(mat, ...)    

mat-linalg.hpp
  has the MatrixOps namespace

  rank: DMatLinAlg<RT> for doing LU decompositions 
  LUdecomp.rank()
  
  eigenvalues:
  Lapack::eigenvalues(&A, &eigenvals); (lapack.hpp, lapack.cpp)
```  
