(This page will be edited during the "**M2 internals**" meeting on May 8-10, 2020.)

##  Topics:
* [[setting up your machine for Macaulay2 development]]
* [[CMake build system]] 
* [[the interpreter and how it is implemented]]
* [[D language]]
* [[adding functions to the engine and interfacing them to the front end|Adding Engine Functions]]
* [[the engine: the class structure (rings, module, gbs, resolutions, computations), engine.h|Class Structure]]
* [[M2 engine examples|M2-engine-examples]]
* [[Unit tests]]
* [[Other internal topics]] (put other bits here for now)

## Further topics:
* documentation system
* testing and debugging
* `tryM2` and `jupyter`

## Projects in the Pipeline & Roadmap (5/10/2020) (if I missed anything, please add)
- eigen branch (Mike and Anton)
- non-commutative Groebner Bases (Mike and Frank)
- benchmark with other garbage collectors
  - look into Julia's [GC](https://github.com/JuliaLang/julia/blob/master/src/gc.h)
  - look for ideas from Gary Furnish's [cgc1](https://github.com/garyfurnish/cgc1)
- using multithreading in more places in the engine
- new functorial ChainComplexExtras package (Mike and Greg)
- documentation
  - presentation: e.g. better LaTeX support
  - content: future documentation workgroup/workshop
- internal improvements (to be discussed next meeting?)
  - documentation: doxygen (sphinx?)
  - renaming things + removing dead code + documenting
- automate interfacing with external libraries
  - use Polymake as a library
  - Arb / MPFI

## Next Internal Events
- Virtual meetings are great 👍
  - Reduced cost of participation and is good for climate change!
- More frequent, but smaller meetings 👍