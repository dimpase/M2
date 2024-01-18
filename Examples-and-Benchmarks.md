The purpose of this page is to accumulate various interesting examples.  Of particular interest is computational benchmarks for various algorithms.  A good benchmark consists of an indexed family of examples such that an algorithm completes in a reasonable amount of time for small values, but fails to complete in a reasonable amount of time for larger values.  These examples can be used to assess progress of code improvement efforts and evaluate alternative algorithms.

# Description

A benchmark ought to include information about the example and any relevant parameters, enough information for a reader to reproduce the calculation, and the runtime of relevant algorithms and hardware specifications of the platform upon which the algorithm was ran.  Multiple algorithms can be ran on a given example, and multiple runs of a given algorithm can be included on the same or different hardware platforms.  In particular, they should be formatted as follows:
1. Example (e.g., ideal(x^n,y^n), n=1,2,...)
2.  Description, pseudocode, or code of the algorithm performed (e.g, "isRegularSequence(x^2,y^2)".  Make sure you provide enough for reproducibility).
  - Platform: Processor Name, Speed (in GHz), #cores/threads (only if parallel processing performed), Memory Type (DDR3, DDR4, etc.), Memory Size (8gigs, 16 gigs, etc.), Page file/swap space used yes/no (Likely no unless your calculation exceed your RAM's capacity)
    - Running time (for various parameters, if relevant) (e.g., n=1: 5s, n=2, 2m).
    - Comments
  - Platform: ... etc.
3. Description of alternative algorithm performed
   - Running time...
etc.

Benchmarks for related tasks can be placed together within the same section.

If you have trouble finding information about your hardware platform, or are missing some other pieces of information don't worry about including all of it.  Some information is better than none, and we can fill out more info as a community.

# Benchmark Pages
## Parallel Processing
Given a number of variables, an exponent, and a number of threads, the following will saturate the maximal ideal raised to the given power with respect to each variable in a different thread:
```
threadedSaturate = method();
threadedSaturate(ZZ, ZZ, ZZ) := (numvars, exponent, numthreads) -> elapsedTime (
    x := symbol x;
    R := ZZ/101[x_0..x_(numvars - 1)];
    m := ideal vars R;
    oldnumthreads := allowableThreads;
    allowableThreads = numthreads;
    tasks := apply(gens R, var -> createTask(
        () -> elapsedTime saturate(m^exponent, var)));
    schedule \ tasks;
    while not all(tasks, isReady) do nanosleep 1000000;
    allowableThreads = oldnumthreads;
    taskResult \ tasks)
```

So for example, `threadedSaturate(4, 5, 4)` will use 4 threads to saturate $(x_0,\dots,x_3)^5$ with respect to $x_3$.
## Local Cohomology

1. ```
R = QQ[x_1..x_6]
I = intersect(ideal(x_1,x_2),ideal(x_3..x_6))
```
2. `localCohom(2,I)
  - Platform: ?
    - Time: 118s