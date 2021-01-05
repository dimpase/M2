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