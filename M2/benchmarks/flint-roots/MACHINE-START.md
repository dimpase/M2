# Machine-precision initialization

All numerical solves now start with a 53-bit `acb_poly_find_roots` call,
including each factor after squarefree decomposition. FLINT 3.5.0 uses its
hardware-double implementation at this precision (with internal fallback where
needed). The previous implementation started at max(64, requested bits + 32),
bypassing this path.

Finite approximations carry forward into higher precision; coefficients are
reconstructed from the original exact values every time. Precision doubles,
with a step at requested bits + 32 before proceeding higher if necessary.
Certification and multiplicity checks are unchanged. A machine-precision start
does not imply that the input coefficients or final roots are limited to 53 bits.

`flint-target` retains the old policy. `benchmark.py --compare-starts` runs
both implementations and MPSolve sequentially in the same session, with the
same deterministic inputs and warm-up/median-of-three protocol. The following
are single-thread backend milliseconds, measured 2026-09-22 on the same
Gentoo/FLINT 3.5.0 machine as the original run. As before, this is a shared,
low-priority run, not a controlled microbenchmark. MPSolve eight-thread timings
are also preserved in the JSON.

| Case | Bits | Previous FLINT | Machine-start FLINT | Speedup | MPSolve |
|---|---:|---:|---:|---:|---:|
| constant | 53 | 0.000 | 0.000 | — | 0.000 |
| zero-root-12 | 53 | 0.003 | 0.003 | 0.95x | 0.456 |
| doc-13 | 53 | 0.291 | 0.250 | 1.16x | 1.485 |
| doc-square-26 | 150 | 0.490 | 0.541 | 0.91x | 13.176 |
| wilkinson-20 | 53 | 2.278 | 1.866 | 1.22x | 2.627 |
| cluster-12 | 150 | 11.000 | 13.508 | 0.81x | 4.594 |
| complex-repeat-12 | 150 | 10.732 | 22.204 | 0.48x | 5.386 |
| wide-scale-10 | 150 | 2.831 | 0.171 | 16.60x | SIGSEGV |
| integer-32 | 53 | 4.115 | 0.904 | 4.55x | 1.590 |
| integer-32-256 | 256 | 8.722 | 3.328 | 2.62x | 2.402 |
| integer-100 | 53 | 41.820 | 7.715 | 5.42x | 5.025 |
| integer-100-256 | 256 | 110.781 | 30.511 | 3.63x | 9.171 |
| integer-256 | 53 | 322.412 | 50.277 | 6.41x | 39.694 |
| rational-32 | 150 | 3.336 | 1.884 | 1.77x | 2.469 |
| complex-double | 53 | 3.481 | 0.923 | 3.77x | 1.892 |
| real-double | 53 | 2.302 | 1.627 | 1.41x | 2.005 |
| complex-mpfr | 150 | 5.499 | 2.205 | 2.49x | 1.816 |
| real-mpfr | 150 | 3.143 | 1.760 | 1.79x | 1.753 |
| roots-of-unity-256 | 53 | 180.209 | 35.937 | 5.01x | 25.018 |

The dense degree-100 and degree-256 cases improve by about 5.4x and 6.4x.
The corresponding MPSolve gaps narrow to about 1.5x and 1.3x. At degree 100
and 256-bit output, FLINT improves about 3.6x but remains about 3.3x slower
than MPSolve. Complex repeated roots regress about 2x: the cheap-start strategy
adds failed numerical stages before exact decomposition. Thus the policy is a
substantial improvement for dense squarefree examples, not a universal speedup.

Validation:

* All 19 benchmark cases return the expected root counts under both FLINT
  policies, retaining certification to the requested accuracy. Root multisets
  agree within the requested precision. MPSolve retains the previously observed
  high-precision zero-root crash; it is not counted as a timing result.
* The M2 wrapper test passes for ZZ, QQ, RR, CC, precision, multiplicities,
  zero roots, constants, rational functions, and multivariable frontend behavior.
* New known-root tests pass for roots separated by 2^-100 (728 working bits),
  roots 2^1500 and 2^-1500 (182 working bits), and repeated complex roots
  (364 working bits), all requesting 150-bit answers. The first two cases cannot
  be resolved solely by ordinary double approximations. Tests verify relative
  error against known roots as well as the returned certification accuracy.

Reproduce with the commands in README. Committed raw measurements:
`measurements/gentoo-machine-start.json`. Full input/output logs:
`/home/dima/tmp/flint-roots-machine-start/`.
