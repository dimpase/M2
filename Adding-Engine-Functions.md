Work in progress. Contributors: Michael Burr, (your-name-here)

## Adding Engine Functions

### Overview

History: Engine is based on (very) old version of C++ (One of Mike's goal is to modernize)

Structure: Three parts: 

1. Engine (C++ code, e directory)

2. Interface (d/dd).  Has interface.dd, connects actual function to m2 interpreter function.  (d is for C code, dd is for C++ code)

3. M2 code.

Parts 1. and 2. compile to executable.

### engine.h

Provides C/C++ functions that the top level Macaulay2 code can call.  Most of the code is contained in files x-* files.  Functions should be named raw<FunctionName> (not within a namespace).  Place the raw<FunctionName> and arguments in the header and the source code in an x-* file.
