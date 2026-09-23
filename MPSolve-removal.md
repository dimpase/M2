# Investigating removal of MPSolve from Macaulay2

This branch contains a FLINT-based root-finding prototype and comparative
benchmarks. **It does not remove MPSolve or change M2's production backend.**
The experiment demonstrates the required operations on representative inputs,
but does not establish a uniformly faster replacement or production readiness.

The experiment started from development commit `1d6b32d07b`. The prototype was
introduced in `60267e854e`; `65823190ff` changed numerical initialization to
machine precision. Measurements below were collected on 2026-09-22, before this
report was assembled on 2026-09-23.

## Scope of the dependency

The source audit found one direct numerical integration:
[`rawRoots` in polyroots.cpp](M2/Macaulay2/e/interface/polyroots.cpp).
The public [`roots` method](M2/Macaulay2/m2/factor.m2) dispatches to it, including
calls from packages. Other root-finding algorithms in packages are not
necessarily MPSolve users merely because they operate on roots.

This entry point accepts univariate polynomials over ZZ, QQ, machine real and
complex numbers, and arbitrary-precision real and complex numbers. Rational
functions use the numerator. The M2 frontend handles a polynomial involving
only one variable in a larger polynomial ring. Precision defaults to 53 bits
for exact coefficients and to the coefficient precision otherwise.

The current native implementation ignores `Unique`, despite its documented
meaning. The prototype preserves that behavior and returns multiplicities;
implementing `Unique => true` would be a separate behavior fix. Root ordering
is unspecified.

Additional MPSolve references concern version reporting, dependency discovery,
fallback builds, linking, distribution licenses, and documentation. Removing
the numerical dependency would require updating those places too.

## Current MPSolve algorithm and arithmetic

M2 selects `MPS_ALGORITHM_SECULAR_GA` and `MPS_OUTPUT_GOAL_APPROXIMATE`. The
secular-equation approach combines Ehrlich–Aberth iteration with regeneration
of a secular representation and adaptive precision. See the
[Bini–Robol algorithm paper](https://doi.org/10.1016/j.cam.2013.04.037) and the
[MPSolve project](https://numpi.dm.unipi.it/scientific-computing-libraries/mpsolve/).

MPSolve's multiprecision real arithmetic uses **GMP `mpf_t`**. Its own `mpc_t`
complex type contains two `mpf_t` components; this is not GNU MPC. See
[MPSolve's complex-number header](https://github.com/robol/MPSolve/blob/master/include/mps/mpc.h).
M2 stores high-precision real components in MPFR and converts them with
`mpfr_get_f` on input and `mpfr_set_f` on output. The benchmark mirrors M2's
`d`, `f`, and `q` coefficient setters and its double/multiprecision result paths.

## FLINT prototype

The standalone implementation is
[`roots.cpp`](M2/benchmarks/flint-roots/roots.cpp). It uses FLINT's Acb
complex-ball polynomial root finder, which applies Durand–Kerner refinement
and validates the approximations. It returns only after all roots have been
isolated and the requested relative accuracy has been certified, then rounds
the midpoints for output. See the
[Acb polynomial root-finding documentation](https://flintlib.org/doc/acb_poly.html#root-finding).

Repeated roots require special treatment because increasing precision alone
will not make the squarefree root finder certify them:

1. For real coefficients, clear rational denominators and use
   `fmpz_poly_factor_squarefree`. Solve each squarefree factor and repeat its
   roots according to the factor's multiplicity.
2. For complex coefficients, first try numerical isolation of the original
   polynomial. Isolating all roots certifies squarefreeness, avoiding an exact
   gcd in the common case. If refinement through twice the target working
   precision does not succeed, perform squarefree decomposition over Q(i)
   with FLINT's number-field/generic-ring interface, then solve each factor.
3. Floating-point inputs become exact dyadic rationals representing their stored
   values. Recreate coefficient balls from this exact data at every precision;
   do not freeze the rounding error from the initial conversion. Higher output
   precision does not recover information already lost when input coefficients
   were rounded.
4. Retain zero roots and multiplicities, return no roots for nonzero constants,
   and reject the zero polynomial.

### Machine-precision initialization

Every numerical solve now starts at 53 bits, including individual factors.
For degree at least two, FLINT 3.5.0's call path is:

```text
acb_poly_find_roots(..., prec = 53)
  -> _acb_poly_find_roots
     -> _acb_poly_find_roots_double
        -> cd_poly_find_roots
```

The double wrapper scales/converts coefficients; FLINT can fall back internally
when double arithmetic does not suffice. Finite approximations are reused at
higher precision. The prototype doubles precision, with an intermediate step
at `max(64, requested_bits + 32)`, and continues until certification succeeds.
For example, a 256-bit request normally tries 53, 106, 212, then 288 bits.
The implementation can be inspected in
[FLINT 3.5.0's find_roots.c](https://github.com/flintlib/flint/blob/v3.5.0/src/acb_poly/find_roots.c).

The original prototype started at `max(64, requested_bits + 32)` and bypassed
the double path. That strategy remains available as `flint-target` for direct
comparison. The current `flint` mode starts at machine precision. No change to
the installed FLINT library was needed.

## Where the benchmark inputs come from

[`benchmark.py`](M2/benchmarks/flint-roots/benchmark.py) generates 19 cases
with Python's fixed random seed `4725`. They are synthetic test cases, not a
corpus extracted from real package workloads:

* The polynomial `x^13 + 5*x^9 + 7*x^4 + x + 1` from M2's
  [`roots` documentation](M2/Macaulay2/packages/Macaulay2Doc/functions/roots-doc.m2),
  and its square.
* Dense random integer polynomials of degrees 32, 100, and 256; some repeated
  at 256-bit output precision. Nonleading coefficients are sampled from
  integers -100 through 100 and the leading coefficient is one.
* Degree-32 rational polynomials, and real/complex polynomials with exactly
  representable dyadic coefficients, using double or multiprecision setters.
* Wilkinson's degree-20 polynomial; 12 roots spaced by `2^-30` near one;
  explicitly repeated complex roots; zero roots; a constant; and `x^256 - 1`.
* A wide-scale polynomial with roots zero and `2^k` for k = -40, -30, ..., 40.

The generator is the authoritative definition of each case. Separate known-root
stress tests use a separation of `2^-100`, magnitudes `2^1500` and `2^-1500`,
and repeated complex roots.

## Measurement protocol

Host: Intel Core Ultra 7 165U, Gentoo Linux 7.0.3, GCC 16.2.0, FLINT 3.5.0,
MPSolve 3.2.3. Runs were sequential, at nice level 19 and idle I/O priority,
on a shared machine. Each backend performs one warm-up and three timed solves;
the reported total is their median. FLINT used one thread; MPSolve was tested
with one and eight. Merely raising FLINT's thread limit does not parallelize
this root finder.

Timings include backend coefficient conversion, preprocessing, solving and
result extraction. They exclude process startup, parsing/printing the input
and output, Python validation, and M2 object conversion. The M2 wrapper's
subprocess overhead is therefore not represented in this table. These are
backend comparisons, not end-to-end M2 timings or controlled microbenchmarks.

The stopping criteria differ: the prototype explicitly requires ball isolation
and accuracy, while the MPSolve path requests approximation. This does not mean
MPSolve lacks error-control machinery; it means the two calls are not asking
for identical output objects or using identical termination checks.

## Benchmark results

The table uses the **same-run comparison after the machine-start change**.
Times are milliseconds. Values displayed as 0.000 are below useful timing
resolution, not literally cost-free.

| Case | Degree | Bits | Previous FLINT | Machine-start FLINT | MPSolve, 1 thread | MPSolve, 8 threads |
|---|---:|---:|---:|---:|---:|---:|
| constant | 0 | 53 | 0.000 | 0.000 | 0.000 | 0.000 |
| zero-root-12 | 12 | 53 | 0.003 | 0.003 | 0.456 | 0.647 |
| doc-13 | 13 | 53 | 0.291 | 0.250 | 1.485 | 1.150 |
| doc-square-26 | 26 | 150 | 0.490 | 0.541 | 13.176 | 10.730 |
| wilkinson-20 | 20 | 53 | 2.278 | 1.866 | 2.627 | 2.874 |
| cluster-12 | 12 | 150 | 11.000 | 13.508 | 4.594 | 4.863 |
| complex-repeat-12 | 12 | 150 | 10.732 | 22.204 | 5.386 | 5.225 |
| wide-scale-10 | 10 | 150 | 2.831 | 0.171 | SIGSEGV | SIGSEGV |
| integer-32 | 32 | 53 | 4.115 | 0.904 | 1.590 | 1.692 |
| integer-32-256 | 32 | 256 | 8.722 | 3.328 | 2.402 | 2.328 |
| integer-100 | 100 | 53 | 41.820 | 7.715 | 5.025 | 4.673 |
| integer-100-256 | 100 | 256 | 110.781 | 30.511 | 9.171 | 9.469 |
| integer-256 | 256 | 53 | 322.412 | 50.277 | 39.694 | 38.754 |
| rational-32 | 32 | 150 | 3.336 | 1.884 | 2.469 | 2.537 |
| complex-double | 32 | 53 | 3.481 | 0.923 | 1.892 | 1.820 |
| real-double | 32 | 53 | 2.302 | 1.627 | 2.005 | 1.479 |
| complex-mpfr | 32 | 150 | 5.499 | 2.205 | 1.816 | 1.988 |
| real-mpfr | 32 | 150 | 3.143 | 1.760 | 1.753 | 1.698 |
| roots-of-unity-256 | 256 | 53 | 180.209 | 35.937 | 25.018 | 23.995 |

Machine initialization improves the dense degree-100 and degree-256 examples
by about **5.4x and 6.4x**. Their gaps to single-threaded MPSolve shrink to about
1.5x and 1.3x. At degree 100 and 256-bit output, FLINT improves about 3.6x but
remains about 3.3x slower. It beats MPSolve on several smaller cases.

It is not a universal improvement: the repeated-complex case becomes about
twice as slow, because extra unsuccessful numerical stages precede exact
factorization. More selective dispatch may improve that case.

Both MPSolve configurations crash on the wide-scale case at 150 bits. The same
input produced SIGSEGV in the existing built M2's native `roots`; the precise
wrapper/library cause was not diagnosed in this experiment. This failure is
not treated as a timing result or evidence of a speedup.

### How much is squarefree preprocessing costing?

For the current machine-start run:

| Case | Recorded preprocessing / total |
|---|---:|
| Degree 100, 53 bits | 0.38% |
| Degree 100, 256 bits | 0.09% |
| Degree 256, 53 bits | 0.15% |
| Squared documentation example | 2.87% |

These are approximate ratios, not isolated profiles of squarefreeness checking:
the numerator is the final trial's preprocessing timer and the denominator is
the median total. Preprocessing includes coefficient conversion and squarefree
decomposition. On complex fallback paths it also includes the unsuccessful
numerical attempts; the roughly 49% figure for the repeated-complex case must
not be attributed entirely to squarefreeness checking. Complex cases certified
directly do not run a separate exact squarefree decomposition.

The real dense-polynomial gap is therefore not explained by squarefree
preprocessing or by MPSolve using more threads. The different iterations,
precision management, and validation requirements are plausible contributors.
Iteration versus certification time has **not** been separately profiled, so
we cannot assign percentages to those causes. Nor do these cases establish a
sharp degree-100 crossover or show density to be the sole determining factor.

## Validation and remaining work

All 19 cases returned the expected root counts with both FLINT policies, with
certification before rounding. Successful MPSolve comparisons agreed as root
multisets within a few target-precision ulps. The harness records counts,
scaled residuals and multiset agreement; residuals alone would not establish
completeness or multiplicities.

The M2 wrapper tests pass for ZZ, QQ, RR and CC, requested precision,
multiplicities, zero roots, constants, rational functions, and the univariate
frontend for a multivariable ring. Known-root stress tests at 150-bit output
pass for separation `2^-100` (728 working bits), roots `2^1500` and `2^-1500`
(182 working bits), and repeated complex roots (364 working bits). These check
relative errors against known roots as well as certification accuracy.

The code is still a prototype. It caps working precision at 32768 bits and
bounds iteration counts. It exits on failure and has no engine-level interrupt
handling or exception-safe cleanup suitable for continued in-process use.
The generic-ring/number-field APIs were tested with FLINT 3.5.0, not all older
versions accepted by M2's current build systems.

Before removing MPSolve:

1. Integrate the FLINT code into `rawRoots`, with RAII cleanup, interruption and
   resource limits, and direct coefficient/result conversions.
2. Establish the minimum supported FLINT version and test platform compatibility.
3. Decide how to fix `Unique` and test error behavior, difficult inputs, and real
   package workloads. Preserve behavior independently of undocumented root order.
4. Run engine, core, package and documentation regression suites; benchmark the
   native integration, not just the out-of-process wrapper.
5. Update CMake and Autotools dependency checks, linking and fallback rules,
   version reporting, packaging/licenses, and documentation attribution.

A selectable backend would allow wider evaluation before changing the default.
The tested functionality makes removal plausible, but neither complete
compatibility nor a uniform performance advantage has been established.

## Reproduce and try it

From a checkout of the `prototype-flint-roots` branch:

```sh
cd M2/benchmarks/flint-roots
nice -n 19 make
nice -n 19 ionice -c 3 python3 benchmark.py --binary ./roots --compare-starts --output results
nice -n 19 ionice -c 3 python3 test_machine_start.py ./roots
export FLINT_ROOTS_BINARY="$PWD/roots"
nice -n 19 ionice -c 3 M2 --script test.m2
```

Build requirements are FLINT, MPSolve, GMP/GMPXX, MPFR and a C++17 compiler;
the benchmark scripts additionally need Python and mpmath. The standalone
comparison still links **both** backends. An existing M2 is needed only for the
M2 wrapper and its tests; building M2 or initializing its submodules is not
necessary for the standalone comparison.

With `FLINT_ROOTS_BINARY` set, start M2 in that directory:

```m2
load "flintRoots.m2"
R = QQ[x]
flintRoots((x^13 + 5*x^9 + 7*x^4 + x + 1)^2, Precision => 150)
```

This defines a separate out-of-process `flintRoots`; it does not override
`roots` or change the installed M2.

## Data and references

* [Prototype and reproduction instructions](M2/benchmarks/flint-roots/README.md).
* [Machine-start comparison](M2/benchmarks/flint-roots/MACHINE-START.md) and
  [raw JSON measurements](M2/benchmarks/flint-roots/measurements/gentoo-machine-start.json).
* [Original measurements](M2/benchmarks/flint-roots/RESULTS.md) and
  [original JSON](M2/benchmarks/flint-roots/measurements/gentoo-flint-3.5.0.json).
  These are from a different run; use the same-run table above for speedup ratios.
* Dario A. Bini and Leonardo Robol, *Solving secular and polynomial equations:
  A multiprecision algorithm*, Journal of Computational and Applied Mathematics
  272 (2014), 276–292. [DOI](https://doi.org/10.1016/j.cam.2013.04.037),
  [author-hosted manuscript](https://web.dm.unipi.it/robol/assets/pdf/secular-paper.pdf).
* [FLINT Acb root-finding API](https://flintlib.org/doc/acb_poly.html#root-finding)
  and [versioned implementation](https://github.com/flintlib/flint/blob/v3.5.0/src/acb_poly/find_roots.c).
* [MPSolve project](https://numpi.dm.unipi.it/scientific-computing-libraries/mpsolve/)
  and [its GMP-based complex arithmetic](https://github.com/robol/MPSolve/blob/master/include/mps/mpc.h).

The original generated inputs and full logs remain locally at
`/home/dima/tmp/flint-roots-benchmark-v4/` and
`/home/dima/tmp/flint-roots-machine-start/`. The committed generator and JSON
summaries are sufficient to reproduce the cases and inspect the reported
measurements without those local directories.
