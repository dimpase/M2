* Potential advisor/consultant(s): Mike Stillman
* Goal: Implement `ZZ/n` for composite `n` in the engine 
* Current status: volunteers welcome!
* Macaulay2 skill level: beginner with some Macaulay2 experience, knowledge of C++ is necessary 
* Mathematical experience: advanced undergraduate 
* Reason(s) to participate: learn Macaulay2 internals, provide a faster implementation of `ZZ/n` to researchers

## Project Description

Currently `ZZ/n` "works" only for prime `n`.   
Implementing `ZZ/n` for composite `n` in the engine would allow fast operations (e.g., linear algebra) over `ZZ/n` for arbitrary `n`. 

### Workaround

Currently one can create a quotient of a polynomial ring with no variables: `ZZ[]/n`. This "works", albeit slowly.

