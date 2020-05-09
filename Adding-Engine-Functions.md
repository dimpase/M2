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

Provides C/C++ functions that the top level Macaulay2 code can call.  Most of the code is contained in files x-* files.  Functions should be named raw{FunctionName} (not within a namespace).  Place the raw{FunctionName} and arguments in the header and the source code in an x-* file.  Recompile after adding changes.

### interface.dd

Add the function to connect the Macaulay2 to the raw function.  export <rawFunctionName>(e:Expr):Expr := (...);  when e is of the right type of object, check length and properties of e.  toExpr(...) is the actual call.  Exceptions are WrongArg{Error Type}(...).  toExpr(Ccode({return type},"raw{FunctionName}(",{arguments separated by commas and ","'s, ")"}.  sefupfun("M2 language name",new function name); can be the same name.  parse.d has Expr definition.


### Macaulay2 
     Calls the M2 language name.  This function can be used within M2 functions (to hide and use the underlying code).  Start with debug Core or raw{function name} = value Core#"private dictionary"#"Function name" to access the function.