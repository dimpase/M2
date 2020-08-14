This documents a way to add [mpfi](https://gforge.inria.fr/projects/mpfi/) to the arsenal of M2. Perhaps also [arb](http://arblib.org/). 

## mpfi ## 

We can work by analogy with `mpfi`.
Before starting, check the license compatibility: some version of GPL is usually OK.
* Modify `M2/INSTALL`.
* `M2/configure.ac` 
** Get `mpfi` on `LIBLIST` (the libraries appear in order of dependency).
** Check that `mpfi.h` is in order: search for `AC_CHECK_HEADER` and `mpfr` to see an example.