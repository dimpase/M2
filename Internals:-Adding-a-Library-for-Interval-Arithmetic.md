This documents a way to add [mpfi](https://gforge.inria.fr/projects/mpfi/) to the arsenal of M2. Perhaps also [arb](http://arblib.org/). 

## mpfi ## 

### Dan Grayson's talk summary ### 
We can work by analogy with `mpfr`.
Before starting, check the license compatibility: some version of GPL is usually OK.
* Modify `M2/INSTALL`.
* `M2/configure.ac` 
  * Get `mpfi` on `LIBLIST` 
  * Check that `mpfi.h` is in order: search for `AC_CHECK_HEADER` and `mpfr` to see an example. (The libraries appear in order of dependency: more dependent first, more independent last. So `-lmpfi` should be go before `-lmpfr`.)
* Create `M2/libraries/mpfi/Makefile.in` (modify a copy of `M2/libraries/mpfr/Makefile.in`)
* Make sure you **run `make` in `M2/`** after modifying `configure.ac` and any of the `Makefile.in` files.
* `grep -r mpfr M2/Macaulay2/*` to see where in source code `mpfr` is used.
  * e.g. `d/version.dd` has  `"mpfr version" => Ccode(constcharstar,"mpfr_version")`
* dichotomy in memory allocation (native vs. garbage collected): see `d/gmp.d` for comment starting with `--We introduce to types...`
* Create something analogous to `RRcell` (see `parse.d`)

### What makes `RR_100` tick? (This may make `RRi` tick.) ###

* Compare `raw RR_100` and `raw RR_53` (53=standard precision)
* `rawRR` in `interface.dd` wraps `IM2_Ring_RRR` --- make something like that: e.g. create `rawRRi` that wraps `rawRingRRi`
* `IM2_Ring_RRR` is in `engine.h` and `x-relem.cpp`. Inspect the code in the latter. 
* Look at `aring-RRR.hpp`
  * Engine's `ARing`s are fast implementations of "coefficient rings". (A polynomial ring is not an ARing. See `aring.hpp` for `DummyRing` --- all methods mentioned there need to be implemented.)
  * Create `aring-RRi.hpp` --- this will house `ARingRRi`. 
  * In `aring.hpp`, add `ring_RRi` and set `ring_top = 17`
  * No worries about memory allocation --- assume all memory is getting allocated without GC, unless `gmp_RR` gets involved.
* Look at `aring-glue.hpp` (no need to make changes here --- just be aware that this is a place where `ARing`s get used).
  * `ring_elem` operations are handled here (at the moment, `ring_elem` is GC-ed).

### autotools ###
The summary of [this commit](https://github.com/Macaulay2/M2/pull/1465/commits/e6b4585ff93500d25567a05fa9d5a4726c0bd517):
* add 1 line to `config/files`
* in `configure.ac` mention `mpfi` in help for `--enable-build-libraries` options
* write `libraries/mpfi/Makefile.in`
    
### cmake ###
Detailed instructions are [here](https://github.com/DanGrayson/Internals/blob/master/cmake-14-8-2020/GUIDE.md).
* `ExternalProject_Add` is what we need to add `mpfi` (modify the corresponding block in `cmake/build-libraries.cmake` for `mpfr`).
  * There are several steps in setting up an external project: e.g. `CONFIGURE_COMMAND` controls the "configure" step, `BUILD_COMMAND` the building, etc.
  * `_ADD_COMPONENT_DEPENDENCY` to declare `mpfi` dependencies.
* Modify `cmake/check-libraries.cmake` and `cmake/FindMPFI.cmake` accordingly.

### Front end ###
(Michael Burr and Anton Leykin)
* changes in `d/` involve `classes.dd`,`expr.d`,`actors2.dd`, `equality.dd`, `parse.d`, `gmp.d`, `gmp_aux.[h,c]` 
  * introduce `RRi`, `RRimutable`, `RRiClass`
  * copy-paste `RR` versions of methods (with minimal edits) whenever errors pop up during a build. 
* `gmp.d` handling `RRi`, `RRimutable`:
  * `leftRR` and `rightRR` get the left/right ends of the interval
  * input methods
  * arithmetic operations
  * comparison operations
* `util.d`
  * `toExpr`
* `gmp1.d`
  * `tostringRRi`
* `interface.dd`
  * `rawToRRi` (is it used anywhere? see. `toRRi`)
* `actors.d`
  * arithmetic on the level of `Expr`
* `actors3.d`
  * `round0(e:Expr):Expr`
* `actors4.d`
  * `interval` (constructor)
  * `toRRi`, `toRR`, `toCC`, etc. (for `Expr`)
* `real.m2` handles the `InexactField` called `RRi` 
* `exports.m2` exports `RRi`, `RRi'`, `toRRi`, `interval`
 
### Promote and lift ### 
  - raw rings/elements (general): `m2/engine.m2`
  - single (raw/front) ring elements: `m2/reals.m2`
  - matrices/lists (general): `m2/modules.m2`, uses `rawPromote` 
  
General questions:
- How should `promote` and `lift` work for intervals? 
  - What is the philosophy for `RR_*`? 
- What is the expected behavior of `new ... from ...` ?
