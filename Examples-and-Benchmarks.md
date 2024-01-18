The purpose of this page is to accumulate various interesting examples.  Of particular interest is computational benchmarks for various algorithms.  A good benchmark consists of an indexed family of examples such that an algorithm completes in a reasonable amount of time for small values, but fails to complete in a reasonable amount of time for larger values.  These examples can be used to assess progress of code improvement efforts and evaluate alternative algorithms.

# Description

A benchmark ought to include information about the example and any relevant parameters, enough information for a reader to reproduce the calculation, and the runtime of relevant algorithms and hardware specifications of the platform upon which the algorithm was ran.  Multiple algorithms can be ran on a given example, and multiple runs of a given algorithm can be included on the same or different hardware platforms.  In particular, they should be formatted as follows:
1. Example (e.g., ideal(x^n,y^n), n=1,2,...)
2.1  Description, pseudocode, or code of the algorithm performed (e.g, "isRegularSequence(x^2,y^2)".  Make sure you provide enough for reproducibility).
  - Platform: Processor Name, Speed (in GHz), #cores/threads (only if parallel processing performed), Memory Type (DDR3, DDR4, etc.), Memory Size (8gigs, 16 gigs, etc.), Page file/swap space used yes/no (Likely no unless your calculation exceed your RAM's capacity)
    - Running time (for various parameters, if relevant) (e.g., n=1: 5s, n=2, 2m).
    - Comments
  - Platform: ... etc.
2.2 Description of alternative algorithm performed
   - Running time...
etc.

Benchmarks for related tasks can be placed together within the same page.

If you have trouble finding information about your hardware platform, or are missing some other pieces of information don't worry about including all of it.  Some information is better than none, and we can fill out more info as a community.

# Benchmark Pages
- Parallel Processing
- Local Cohomology