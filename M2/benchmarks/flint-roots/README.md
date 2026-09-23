# FLINT root backend experiment

All numerical MPSolve integration in M2 is concentrated in
`Macaulay2/e/interface/polyroots.cpp::rawRoots`. `m2/factor.m2` routes `roots`
through it, including package callers. The other direct MPSolve header use is
version reporting (`d/version.dd`); CMake and Autotools discover/link the library.
There is no separate MPSolve implementation for each M2 package to replace.

The numerical operation can be implemented using FLINT for all supported
coefficient domains: ZZ, QQ, machine real/complex, and arbitrary-precision
real/complex. Fraction fields use the numerator; the M2 frontend also flattens
polynomials involving just one variable in a larger ring. This prototype covers
these behaviors, but is not a production replacement or a patch removing MPSolve.

## Algorithm

* Real coefficients: clear rational denominators, factor squarefree using
  `fmpz_poly_factor_squarefree`, isolate each factor with `acb_poly_find_roots`,
  repeat roots according to multiplicity.
* Complex coefficients: first attempt certified isolation of the original
  polynomial. Isolating every root certifies squarefreeness and avoids exact
  preprocessing. If refinement through twice the target working precision does not suffice, perform exact
  squarefree decomposition over Q(i), using FLINT's number-field/generic ring
  interface, then isolate the factors.
* Convert floating-point coefficients to **exact dyadic rationals**, representing
  their stored bits, not an uncertainty interval. At each working precision,
  recreate coefficient balls from exact data. Start every numerical solve at **53 bits**, activating FLINT's hardware-double
  path for degree at least two. Reuse finite root approximations while doubling
  precision (with an intermediate step at the requested precision plus 32 guard
  bits) until every root is isolated with at least the
  requested relative accuracy. Round returned midpoints to the requested bits.
* Zero roots and multiplicities are retained. Nonzero constants return no roots;
  the zero polynomial is rejected. Root ordering is unspecified.

The existing `rawRoots` ignores `Unique`. This experiment deliberately retains
multiplicities even with `Unique => true`; fixing that documented option would
be a separate behavior change. A native integration could cheaply implement it
from the squarefree exponents.

FLINT documents that its Acb root finder assumes squarefreeness:
https://flintlib.org/doc/acb_poly.html#root-finding
Repeated roots cannot simply be passed to that routine with increasing precision.

## Build and try from M2

Requires FLINT (tested with 3.5.0), MPSolve (3.2.3), GMP/GMPXX, MPFR, a C++17
compiler, and Python with mpmath for the benchmarks. The older FLINT versions
accepted by M2's build configurations have not been verified for the generic
number-field APIs used here.

From this directory:

```sh
nice -n 19 make
export FLINT_ROOTS_BINARY="$PWD/roots"
nice -n 19 ionice -c 3 M2 --script test.m2
```

In an interactive M2 session in this directory:

```m2
load "flintRoots.m2"
R = QQ[x]
flintRoots((x^13 + 5*x^9 + 7*x^4 + x + 1)^2, Precision => 150)
```

`flintRoots` is an **out-of-process prototype**, not a replacement for `roots`.
It serializes exact or round-trippable coefficients, calls the standalone
executable once, and returns M2 complex numbers at the requested precision.
Its process-startup and serialization costs are excluded from the backend
benchmark; do not compare wrapper wall times with native `roots` as if they
were engine timings. Neither the installed M2 nor its build is modified.

## Reproduce the measurements

```sh
nice -n 19 ionice -c 3 python3 benchmark.py --binary ./roots --compare-starts --output results
nice -n 19 ionice -c 3 python3 test_machine_start.py ./roots
```

Each backend invocation performs one warm-up and three timed solves; report the
median of the latter. Timings include backend coefficient conversion, squarefree
preprocessing, solving, and result extraction, but exclude file parsing, printing,
Python validation, process startup, and M2's own object conversions. The MPSolve
path mirrors the existing secular-GA algorithm, APPROXIMATE goal and d/f/q input
setters, including its separate double and multiprecision result extraction.
MPSolve is tested with 1 and 8 threads; FLINT with 1 (this Acb root algorithm is
not made parallel simply by setting an 8-thread limit). Runs are sequential,
at nice 19 and idle I/O priority, on a shared machine. Ratios are indicative,
not controlled hardware benchmarks. Constants are below useful timing resolution.

All polynomial coefficients are generated deterministically. Validation records
root counts, scaled polynomial residuals, and greedy full-multiset agreement
with MPSolve at higher comparison precision. The FLINT implementation additionally
requires certified isolation and requested accuracy before returning. Counts
alone or small residuals would not establish correct root multiplicities.

See `MACHINE-START.md` for the improved initialization and a direct comparison
with the previous strategy. The original results remain in `RESULTS.md` and
`measurements/gentoo-flint-3.5.0.json`. Raw inputs and logs
for the measured run are in `/home/dima/tmp/flint-roots-benchmark-v4/`.

## Limits and migration work

This standalone prototype exits on errors and does not provide engine-level
interrupt handling or exception-safe cleanup for continued use after a failure.
It caps working precision at 32768 bits and numerical iterations per attempt;
these are prototype bounds, not completeness guarantees. Integrating it into
`rawRoots` requires RAII cleanup, interruption/resource limits, conversion tests,
minimum-version checks, and package/documentation regression runs. Tests exercise
representative inputs, not every possible polynomial or every package caller.
`test.m2` passes against the local built M2, covering all four public coefficient
domains, requested precision, repeated/zero roots, constants, errors, rational
functions, and the univariate-in-multivariable frontend.

A complete removal would also update both build systems, version reporting,
licenses/packaging and the MPSolve attribution in the roots documentation.
The measured slowdowns on dense polynomials argue against an unconditional
switch solely for speed. A selectable backend is a more cautious next step.
