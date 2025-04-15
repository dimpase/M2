This is a list of previous, upcoming, and proposed breaking changes in the Core of Macaulay2, along with a reference to when and where the change occurred. This is not intended to be an exhaustive list, but focus on the major changes.

### Proposed Changes

- [#3596](https://github.com/Macaulay2/M2/issues/3596): `genericMatrix` should be row major
- [#3194](https://github.com/Macaulay2/M2/issues/3194): operators for `S_+`, `<v,u>`, and `f^#`
- [#1978](https://github.com/Macaulay2/M2/issues/1978): `{1..5}` as syntax for `toList(1..5)`
- [#1608](https://github.com/Macaulay2/M2/issues/1608) and [#1455](https://github.com/Macaulay2/M2/issues/1455#issuecomment-2669543078): operations on `MutableList` should be in-place

### Upcoming Changes
These changes are currently in effect in the `development` branch, to be evaluated until the next release.

- v1.25.05:
  - [#3550](https://github.com/Macaulay2/M2/pull/3550): `Matrix \\ Matrix` is now a shortcut for `quotient'(Matrix, Matrix)`.
    The previous functionality is still available via `Matrix // Matrix`, which is a shortcut for
    `quotient(Matrix, Matrix)`. Additionally, both methods now work for maps of non-free modules.

### Previous Changes
Eventually, the most important breaking changes should be listed here. For now, see [changes to Macaulay2, by version](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_changes_spto_sp__Macaulay2_cm_spby_spversion.html).

- v1.24.11:
  - [#3519](https://github.com/Macaulay2/M2/pull/3519): the behavior of `basis` over tower rings has changed. Previously basis was computed
    over the most recent coefficient ring, but now it is computed over the first coefficient ring.
    Previous behavior can be mimicked by passing the option `basis(..., Variables => gens R)`.

### Rejected Changes

These are mainly listed for posterity.

- [#2336](https://github.com/Macaulay2/M2/issues/2336): change precedence of `Ring Array`