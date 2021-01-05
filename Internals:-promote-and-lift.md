## Top-level

The commands `promote` and `lift` are usually for when we have a natural map of rings A --> B. In this situation, `promote` applies the map to an element of A, and `lift` computes a preimage (typically some sort of normal form.) 

```macaulay2
A=QQ[x]
B=A[y]
elem1 = y^3 -- in B
C=B/(x^2-y^3)
elem2 = x^3 -- in A
methods symbol +
elem3 = elem1+elem2 -- in B
elem4 = promote(elem3,C) -- x^3+x^2 in C
elem5 = lift(elem4,B) -- in B
```

In the line `elem3 = elem1+elem2 `, new methods `(+, B, A)` and `(+, B, B)` are created behind the scenes and stashed in the youngest object `B` as described [here](https://github.com/Macaulay2/M2/wiki/Internals%3A-inheritance-%28of-M2-types%29). Type `code (symbol +, RingElement, RingElement)` to see another use of `promote` in this case.

Examples of natural ring maps (from [aring-glue.hpp](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/e/aring-glue.hpp)):
  *  ZZ --> R, for any R
  *  QQ --> RR --> CC
  *  ZZ --> ZZ/p
  *  ZZ/p --> GF(p^n)
  *  GF(p^m) --> GF(p^n), where m divides n
  *  A --> A[vars]/I
  *  A[vars]/J --> A[vars]/I  (assumption: I contains J).

There are some oddities due to floating-point:

```macaulay2
x=1e-16
y=1+x -- not representable w/ default 53 bits of precision
lift(y, ZZ) -- works
lift(x, ZZ) -- error
```

## Engine

Complicated due to lack of multiple dispatch in C++. Roughly speaking, the target ring controls the implementation. The meat is in [aring-glue.hpp](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/e/aring-glue.hpp) (`RingPromoter` namespace) and [aring-translate.hpp](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/e/aring-translate.hpp).