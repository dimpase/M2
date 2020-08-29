Work in progress. Contributors: Michael Burr, (your-name-here)

## Adding Engine Functions

### Overview

History: The engine is based on an old version of C++.  The engine was originally designed to be fast and to include only the most important things.  It has been growing in size since then to include more.

Project: Modernize the engine

Structure: The engine consists of three parts: 

1. The engine (C++ code).  This is contained in the e directory.

2. The interface (d/dd).  This is contained in the d directory.  The file interface.dd connects actual functions to the m2 interpreter functions.  (Here, d connects to C code while dd connects to C++ code).

3. The M2 code.

Parts 1. and 2. compile to executable.

### engine.h

Provides C/C++ functions that the top level Macaulay2 code can call.  Most of the code is contained in files x-&lt;FileName&gt;.cpp files.  The functions should be named raw&lt;FunctionName&gt; (not within a namespace).  The raw&lt;FunctionName&gt; and arguments should be in the engine.h header and the source code in an x-&lt;FileName&gt;.cpp file.  Recompile after adding changes.

### interface.dd

Add the function to connect the Macaulay2 to the raw function.  Start with the command export &lt;rawFunctionName&gt;(e:Expr):Expr := (...);  Then, perform tests to determine when e is the right type of object, e.g., the length and properties of e.  Use toExpr(...) to make the actual C/C++ call.  The details of the toExpr(...) call are toExpr(Ccode(&lt;return type&gt;,"raw&lt;FunctionName&gt;(",&lt;arguments separated by commas and ","'s, ")"&gt;;.  Exceptions should be raised using functions of the form WrongArg&lt;Error Type&gt;(...).  Finally, use setupfun("&lt;M2 language name&gt;",&lt;rawFunctionName&gt;);  The functions need to be exported so that you can use in another d file, otherwise, no export is needed.

Potential Confusion: There are three names which are often all the same (but not required).  The function setupfun connects the name from within M2 to the function in interface.dd.  The function toExpr makes the call to the engine.

Side Note: See parse.d for the lengthy definition of Expr.

### Macaulay2

Macaulay2 can call the name from interface.dd to run the code.  Often these are used within an M2 functions to hide the underlying C/C++ code.

Accessing Functions: There are a few main ways to access the functions created in the interface.

1. Start with debug Core in M2.  Then, the function can be accessed directly.  Alternately,

2. Assign the function directly with raw&lt;function name&gt; = value Core#"private dictionary"#&lt;Function name&gt;

Side Notes: There are also raw versions of data types which can be explored (with debug Core).  There are alternate ways to access the functions, but the approaches above include more data about the functions.