# Measured results

2026-09-22, Intel Core Ultra 7 165U, Gentoo Linux 7.0.3, GCC 16.2.0,
FLINT 3.5.0, MPSolve 3.2.3. Median of three warmed solves, milliseconds.
Source baseline: M2 development `1d6b32d07b`; audited local branch `8031ebdb88`
has the same MPSolve root implementation. See README for methodology and limits.

| Case | Degree | Bits | FLINT (1 thread) | MPSolve (1 thread) | MPSolve (8 threads) |
|---|---:|---:|---:|---:|---:|
| constant | 0 | 53 | 0.000 | 0.000 | 0.000 |
| zero-root-12 | 12 | 53 | 0.005 | 0.577 | 0.606 |
| doc-13 | 13 | 53 | 0.497 | 1.135 | 1.163 |
| doc-square-26 | 26 | 150 | 0.498 | 13.597 | 11.597 |
| wilkinson-20 | 20 | 53 | 2.335 | 2.578 | 2.747 |
| cluster-12 | 12 | 150 | 11.942 | 5.021 | 4.721 |
| complex-repeat-12 | 12 | 150 | 12.608 | 5.583 | 5.279 |
| wide-scale-10 | 10 | 150 | 3.127 | SIGSEGV | SIGSEGV |
| integer-32 | 32 | 53 | 3.887 | 1.853 | 1.640 |
| integer-32-256 | 32 | 256 | 8.774 | 2.562 | 2.344 |
| integer-100 | 100 | 53 | 39.230 | 5.508 | 4.957 |
| integer-100-256 | 100 | 256 | 118.088 | 10.384 | 10.816 |
| integer-256 | 256 | 53 | 365.004 | 45.064 | 50.449 |
| rational-32 | 32 | 150 | 4.042 | 2.767 | 2.527 |
| complex-double | 32 | 53 | 5.277 | 1.845 | 1.586 |
| real-double | 32 | 53 | 2.248 | 2.096 | 1.789 |
| complex-mpfr | 32 | 150 | 5.637 | 2.206 | 1.789 |
| real-mpfr | 32 | 150 | 3.246 | 1.923 | 1.915 |
| roots-of-unity-256 | 256 | 53 | 199.171 | 23.129 | 25.205 |

FLINT returned the expected number of roots on all 19 cases, with certified
isolation at the requested precision before rounding. Every successful MPSolve
comparison agreed as a root multiset to within a few target-precision ulps.
Both sides returned residuals consistent with the requested output precision.
The clustered degree-12 example required 728 working bits for a 150-bit result.

FLINT wins on the degree-13 documentation example and, particularly, its square.
It loses on degree-100/256 dense polynomials and most of the random complex
cases. For complex repeated roots, trying numerical isolation before exact
factorization adds overhead; a different dispatch policy may improve that case.
An earlier always-factor-complex prototype spent 0.19–0.26 s on degree-32
complex inputs; certified isolation first removes most of that unnecessary cost.

The wide-scale case is x times the product of (x - 2^k) for
k = -40, -30, ..., 40 at 150 bits. Both MPSolve harness configurations crash.
The same input also produced SIGSEGV in the existing built M2's native `roots`,
so this is not merely a prototype-only failure. The cause of that existing
wrapper/library failure was not diagnosed here. Its timings are excluded from
performance comparisons. FLINT handles it, including the zero root.

Conclusion: there is no missing mathematical operation preventing removal of
MPSolve, but the measured prototype does not justify promising a uniformly
faster replacement. Native integration and wider package tests remain necessary
before changing M2's default backend or removing its dependency.
