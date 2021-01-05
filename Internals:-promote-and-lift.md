The commands `promote` and `lift` are usually for when we have a natural map of rings A --> B. In this situation, `promote` applies the map to an element of A, and `lift` computes a preimage (typically some sort of normal form.) 

```macaulay2
A = QQ[x]
B = A[y]
elem1 = y^3 -- in B
C = B/(x^2-y^3)
elem2 = 1/2*x^3 -- in A
elem3 = elem1 + elem2 -- C
lift(elem3, B) -- y+x^3 in B
```

When we add `elem1` and `elem2` as above, new methods `(+, B, A)` and `(+, B, B)` are created behind the scenes and stashed in the youngest object `B` as described [here](https://github.com/Macaulay2/M2/wiki/Internals%3A-inheritance-%28of-M2-types%29). Type `code (symbol +, RingElement, RingElement)` to see the usage of `promote`.

