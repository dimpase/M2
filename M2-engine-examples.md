Mike gave an overview of various parts of the engine (located in `M2/Macaulay2/e/`), through specific examples and files below.

## Engine code

* `debug.hpp`: Useful for debugging without going into debugger. All objects have a buffer, and `text_out()` method. One can look up the types of top-level M2-objects which can be displayed this way, and then add print statements (using `std::cout`) in a source file, e.g. `matrix.cpp`, to debug methods.

  * For immutable objects (e.g. matrices/vectors), use `copy_vec` to create copies.

  * Need to add `#include` files, e.g. `#include "debug.hpp"`, `#include <iostream>`

  * Project: change occurrences of `buffer` in `debug.hpp` to C++ o-streams.

* Various types of objects: `Ring`, `ARing` types, `ring_elem` (a union struct, not as safe, involves virtual function calls, has explicit constructors), `RingElement` (raw ring element class)

* `aring-zz-gmp.hpp`: wrapper around gmp
  * mpz: `init`, `clear`, `set` methods
  * Not using C++ interface due to memory allocation/performance issues. 
  * `elem_text_out`: display ring elements

* `aring-gf-flint.hpp`: similar interface as above, for flint

* `mat.hpp`
  * `MutableMatrix` class: abstract class
  * Operations: row/column operations, add/subtract matrices, eigenvalues, SVD, LU, det

* `mutablemat-defs.hpp`
  * `DMat`: Dense matrix, takes RT (ring type)

### (Templated) Types:

* MutableMatrix : front end object, abstract class
  * MutableMat\<MT\> : concrete realization
* RT : ARings.
* DMat\<RT\>
* SMat\<RT\>

* `ConcreteRing` type: only has one piece of data, wrapper to allow virtual function calls. 

Currently: RT is carried through all types (to work with various interfaces, e.g. flint, LAPACK)

Project: consistent naming system (MutableMatrix and MutableMat vs Ring and ConcreteRing. Proposed fix: MutableMatrix -> M2MutableMatrix, MutableMat -> MutableMatrix.)

### GenerateD.m2

Automates creation of code in D language (e.g. for use in `interface.dd`)

### Engine code (part 2)

* `comp.hpp`: Computation class (start, stop conditions). Two types: GBComputation and ResolutionComputation.

* GBComputation (`get_gb()`, `get_mingens()`, etc.). If cannot cast to polynomial ring, determine if ring is ZZ (-> Hermite form) or a field (-> Gaussian elimination), else error "GB computation for non-polynomial rings not yet re-implemented". Switch cases for different strategies: default is gbA (`binomialGB_comp` is defunct). Finally, `intern`'s the result for display.

* ResolutionComputation (`betti_init()`, `betti_display()`, etc.). Again cast to polynomial ring, and further checks if Heft vectors are positive, and if the module is homogeneous. Similarly, switch cases: comp(), res_comp, gbres_comp, or fast non-minimal resolution. Betti table display handled in `betti.hpp`.

* F4 algorithm: associated files in `f4` directory.