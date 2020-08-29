Work in progress. Contributors: Gwyn Whieldon, (your-name-here)

## D Language

Files for internals workshop are available at [Internals](https://github.com/DanGrayson/Internals). First exercise of the day is available [here](https://github.com/DanGrayson/Internals/blob/master/dan/lecture%202%20exercises.txt). A walkthrough of the syntax in the Makefile referenced by the exercise is given below.

**Note that a successfully built version of M2 is a prerequisite for today's exercises.**

### Comparing Translation of D Language into a C Code File

A sample Makefile for illustrating syntax is [here](https://github.com/DanGrayson/Internals/blob/master/dan/D%20language/Makefile)

Be sure that `scc1` is on your path for running the exercises. Run `make` in the D language directory and examine the resulting files from translating foo.d into foo-tmp.c via the Makefile above.

* Do not have to declare variable names ahead of time. Have both an `=` (assignment) and `:=` (assignment and creation), along with `::=` for definition of macros.
* foo-tmp.c is translated into foo.d by the compiler
* In the translated C file, b is declared (`static` means it is not exported) near the top, and `b:=1` later in the file (the C version of `b:=true`).
* The variable c is exported (so not declared static), and `foo_c` indicates that it taken from foo.d
* Ccode keyword gives a macro that literally translates the arguments into C code. In this case, we have defined the meaning of `+` via this macro.
* `if __ then __ else` is an expression, rather than a statement. The line `i := if b then 11 else 22` was translated into a control statement that assigns a temporary variable `_tmp`, which is then assigned to `i`.
  * This has no impact on performance/speed.
* The variable X is defining a struct with two variables (both integers). This variable doesn't appear in foo-tmp.c. What happened? Let's go look in foo-exports.h to see what happened.
  * Looking at the `\* typedefs *\` section, we can see the variable `X_struct`.
  * Looking down into the `\* struct types *\` though, we see that `X_struct` doesn't have a type code assigned.
  * The `+` sign included in the struct is what adds the type code assignment.
* Variables Y and Z are also both structs, where Y has two `int` and a `char` as inputs, and Z just has two `int`.
  * U is defined to be Y or Z (these are different types, can create functions that pass arguments into different functions based on type), declared to be a tagged union.
  * Three keywords (`when`, `if`, `do`) here worth noting in D language:
    * `when` takes variable u, and checks:
    * `if` y is of type Y, then it returns (via `do`) y.a
    * `if` z is of type Z, then it returns (via `do`) z.d
  * This definition of U is turned into a switch statement based on type with cases in the C code.

## Tags Files and Their Use

The exercises go through using `tags-search` in emacs. Returns answers in logical order (rather than, say, alphabetical.)

### Going through actors3.d file

* Using `tags-search`, finding details on `sin` function. Note the `when`, `if`, `do`, `else` syntax based on type, returning appropriate answers based on type (complex, real, integer, rational).
* Exercises show how to run the version of M2 that you're building in emacs.
  * Using meta-x compile in emacs, we recompile the file (in d directory) but didn't produce a new version of the program.
  * Have to go back to the [build-directory]/Macaulay2/bin and recompile the program with `make`.
  * Next exercise is to add a new function to the file actors3.d and expose it at the top level (add it to the `exports.m2` file).
  * `Ctrl-X v =` will show you differences between your file and last git commit.