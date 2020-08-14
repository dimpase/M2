This documents a way to add [mpfi](https://gforge.inria.fr/projects/mpfi/) to the arsenal of M2. Perhaps also [arb](http://arblib.org/). 

## mpfi ## 

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
* `rawRR` in `interface.dd` wraps `IM2_Ring_RRR` --- make something like that: e.g. create `rawRRi` that wraps `rawRRi`
* `IM2_Ring_RRR` is in `engine.h` and `x-relem.cpp`. Inspect the code in the latter. 
* Look at `aring-RRR.hpp`
  * Engine's `ARing`s are fast implementations of "coefficient rings". (A polynomial ring is not an ARing. See `aring.hpp` for `DummyRing` --- all methods mentioned there need to be implemented.)
  * Create `aring-RRi.hpp` --- this will house `ARingRRi`. 
  * No worries about memory allocation --- assume all memory is getting allocated without GC, unless `gmp_RR` gets involved.
* Look at `aring-glue.hpp` (no need to make changes here --- just be aware that this is a place where `ARing`s get used).
  * `ring_elem` operations are handled here (at the moment, `ring_elem` is GC-ed).
   
### cmake ###
Detailed instructions are [here](https://github.com/DanGrayson/Internals/blob/master/cmake-14-8-2020/GUIDE.md).
* `ExternalProject_Add` is what we need to add `mpfi` (modify the corresponding block in `cmake/build-libraries.cmake` for `mpfr`).