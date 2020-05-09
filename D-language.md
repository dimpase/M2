Work in progress. Contributors: Gwyn Whieldon, (your-name-here)

## D Language

Files for internals workshop are available at [Internals](https://github.com/DanGrayson/Internals). First exercise of the day is available [here](https://github.com/DanGrayson/Internals/blob/master/dan/lecture%202%20exercises.txt). Note that a successfully built version of M2 is a prerequisite for today's exercises.

A sample Makefile for illustrating syntax is [here](https://github.com/DanGrayson/Internals/blob/master/dan/D%20language/Makefile)

### Comparing Translation of D Language into a C Code File

* Do not have to declare variable names ahead of time. Have both an "=" and ":=", along with "::=" for definition of macros.
* foo-tmp.c is translated into foo.d by the compiler
* In the translated C file, b is declared ("static" means it is not exported) near the top, and b:=1 later in the file (e.g. b:=true).
* The variable c is exported (so not declared static), and "foo_c" indicates that it taken from foo.d
* Ccode keyword gives a macro that literally translates the arguments into C code. In this case, we have defined the meaning of "+" via this macro.
* "if __ then __ else" is an expression, rather than a statement. The 