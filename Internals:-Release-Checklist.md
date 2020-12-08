Before every release:
- [ ] uncategorized packages should get a keyword:
```m2
i23 : select(separate_" " version#"packages", p -> (readPackage p)#Keywords === {"Uncategorized"})

o23 = {SpecialFanoFourfolds, GKMVarieties}
```
- [ ] DebuggingMode should be turned off in packages:
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