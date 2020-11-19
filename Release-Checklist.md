efore every release:
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
- [ ] M2-emacs and other syntax highlighting files should be updated