Before every release:
- [ ] uncategorized packages should get a keyword:
```m2
i23 : select(separate_" " version#"packages", p -> (readPackage p)#Keywords === {"Uncategorized"})

o23 = {SpecialFanoFourfolds, GKMVarieties}
```
- [x] check existing keywords for sensibility and near duplicates
```m2
i11 : stack sort unique flatten apply(separate_" " version#"packages", p -> (readPackage p)#Keywords)

o11 = Algebraic Geometry
      Algebraic Number Theory
      Algebraic Statistics
      Applied Algebraic Geometry
      Combinatorial Commutative Algebra
      Combinatorics
      Commutative Algebra
      CommutativeAlgebra
      Convex Geometry
      D-modules
      Deformation Theory
      Edge Ideals
      Equivariant Cohomology
      Examples and Random Objects
      Flag Varieties
      Graph Theory
      Groebner Basis Algorithms
      Group Theory
      Homological Algebra
      Interfaces
      Intersection Theory
      Lie Groups and Lie Algebras
      Linear Algebra
      Matroids
      Miscellaneous
      Noncommutative Algebra
      Numerical Algebraic Geometry
      Numerical Linear Algebra
      Real Algebraic Geometry
      Representation Theory
      Statistics
      Toric Geometry
      Tropical Geometry
      Uncategorized
```

- [x] DebuggingMode should be turned off in packages:
```m2
i24 : select(separate_" " version#"packages", p -> (readPackage p)#DebuggingMode)

o24 = {RationalMaps, RelativeCanonicalResolution, SlackIdeals, PencilsOfQuadrics}
```
- [ ] packages should have a top level node:
```m2
i10 : select(separate_" " version#"packages", p -> try (fetchRawDocumentation makeDocumentTag p).Description === {} else false)

o10 = {Browse, SchurFunctors, ChainComplexExtras, OpenMath, SCSCP, Graphs,
      --------------------------------------------------------------------------
      RandomPlaneCurves, RandomCurves, SectionRing, Hadamard}
```
- [ ] M2-emacs and other syntax highlighting files should be updated