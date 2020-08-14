This documents a way to add [mpfi](https://gforge.inria.fr/projects/mpfi/) to the arsenal of M2. Perhaps also [arb](http://arblib.org/). 

## mpfi ## 

We can work by analogy with `mpfi`.
Before starting, check the license compatibility: some version of GPL is usually OK.
* Modify `M2/INSTALL`.
* `M2/configure.ac` 
  * Get `mpfi` on `LIBLIST` (the libraries appear in order of dependency).
  * Check that `mpfi.h` is in order: search for `AC_CHECK_HEADER` and `mpfr` to see an example.
* Create `M2/libraries/mpfi/Makefile.in` (modify a copy of `M2/libraries/mpfr/Makefile.in`)
* Make sure you **run `make` in `M2/`** after modifying `configure.ac` and any of the `Makefile.in` files.
* `grep -r mpfr M2/Macaulay2/*` to see where in source code `mpfr` is used.
  * e.g. `d/version.dd` has  `"mpfr version" => Ccode(constcharstar,"mpfr_version")`
* dichotomy in memory allocation (native vs. garbage collected): see `d/gmp.d` for comment starting with `--We introduce to types...`
* Create something analogous to `RRcell` (see `parce.d`)