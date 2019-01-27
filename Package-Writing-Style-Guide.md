* General recommendations :
    * Any violation of the guide is allowed if it enhances readability.

* Naming conventions :
    * Names representing types must be nouns and written in mixed case starting with upper case.
    * Names representing optional arguments should be capitalized.
    * Variable names must be in mixed case starting with lower case.
    * Names representing methods must be verbs and written in mixed case starting with lower case.
      They should not include the name of the type of object expected as argument, since the idea
      of such methods is that they are mathematical abstractions that act on a variety of types of
      mathematical object.
    * The prefix "is" should be used for Boolean variables and methods.  Examples:
         * `isPolynomialRing`, `isPrimary`, `isPrime`, `isPrimitive`
    * Abbreviations in names should be avoided.
    * Naming of keys in hash tables:
        * Use existing symbols, when possible.  Examples:
             * `source` and `target`, as keys for the source and target of a map
    * Naming of optional arguments:
        * Names of optional arguments should be capitalized
        * Use existing names, when possible.  Examples:
            * `Verify` : whether to check that a result is correct or well defined
            * `Verbose` : whether to print extra information

* Use of types
    * Do not use an object of one type to "represent" an object of another.
         * Example: don't use a matrix to represent the submodule spanned by its columns.
    * Do not introduce a function that performs two consecutive operations, when it would be 
           clearer to factor it into a composite of two functions.  If necessary, introduce
           a new type to serve as the type of the intermediate result.
    * It is usually a mistake to test whether the class of an object is equal to a certain class,
       because that disables inheritance.  In other words, instead of writing something like
       `class x === T`, write `instance(x,T)`.

* Algorithms
    * Do not convert an order n algorithm into an order n^2 algorithm by repeated
      concatenation of lists or of matrices.  Similarly, do not repeatedly append or prepend
      something to a list, and do not repeatedly remove single items from a list.
      Hash tables are your friend here. 
      Notice also that the `for ... list ...` command offers a convenient way to make a list.

* Order of arguments:
    * Functions should take arguments in increasing order of complexity.  For example, if the 
      arguments are an integer and a module, put the integer first.
    * The argument upon which the function mainly acts should go last.

* Package configuration options
    * Package configuration options should be restricted to options that can sensibly be set
      to a single value for the user's whole session.

* Solutions to puzzles:
    * To get a user symbol, such as "x", use ```getSymbol "x"```.  To get n user variables starting with
      "a", use ```vars(0 ..< n)```.
    * To control the order of loading of imported packages ("PackageImports" option) and exported
      packages ("PackageExports" option) while the current package is being loaded, mention the exported
      packages in the list of imported packages, and juggle the sequence of imported packages.
 
* Behavior of code:
    * Packages should not print.
    * Errors should be indicated by calling the function `error`.
    * A package should set no variables in the User dictionary without an explicit request from
      the user.
        * The function `use` should never be used in a package, unless the ring contains no user variables.
        * The function `vars` should not be used in a package.
        * To avoid setting user variables when creating a polynomial ring, use something like
          ```QQ(monoid[getSymbol "a"])``` instead of ```QQ[getSymbol "a"]```
    * Any names of variables in rings created by the package that get exposed to the user through
      returned values, directly or indirectly, should be accessible to the user.
      So use ```QQ(monoid[getSymbol "a"])``` or ```QQ(monoid[vars 0])``` instead of ```QQ[a]```.

* Miscellaneous :
    * Avoid redundant parentheses.  Write `f x` instead of `f(x)`.
    * Don't test a Boolean value for equality with `true` or `false`.
    * Avoid the use of `return`, especially on the last line of a function.
    * The use of magic numbers in code should be avoided.
    * Packages should never export or protect single characters.
    * Variables must never have dual meaning.
    * Use of global variables should be minimized.
    * Many things you'll be tempted to type more than once have abbreviations.  For example,
      when R is a ring, then `first entries vars R` can be shortened to `gens R`.
    * Don't use braces `{ ... ; ... ; ... }` for blocks of code where you don't intend to make a list.
      Instead, write `( ... ; ... ; ... )`.

* Layout :
    * The incompleteness of split lines must be made obvious: break after a comma, break after an
      operator.

* White space :
    * Contents of regions delimited by parentheses, braces, or brackets that consist of multiple lines
      should be indented more than the surrounding lines, with the same indentation for every line.
    * Operators should be surrounded by a space character.
        * But ```n = n+1;``` doesn't look so bad, so maybe this should apply just to loose operators.
    * Commas should be followed by a white space.
        * But ```QQ[x,y,z]``` looks fine...
    * Semicolons should be followed by a space character, but not at the end of a line.
    * Blank lines are not needed.

* Documentation:
    * Each exported data type, method, and function must have a documentation page.  
    * Each documentation page should have an example.
    * Document the type of the return value of method functions, so the documentation generator
      can include those methods in the documentation of the type of the return value.
         * Example: ```resolution Module := ChainComplex => o -> (M) -> (...)```
    * Don't put blocks of example code adjacent to each other.  Merge them, or add some 
      text between them.
    * The "usage" forms for functions don't need to be in the form of assignment statements.
    * Document output values in-line.
    * Do not reload the current package in example code, because its source code might
      not be on the path of the user installing it.
    * Start each sentence with an English word, not an identifier or a symbol.
    * Don't use Macaulay2 identifiers as English words.
    * Don't capitalize English words such as "list" or "tally", even though there are classes in
      Macaulay2 whose names are "List" and "Tally", unless you intend to refer to those classes.

* Comments :
    * Delete commented-out code.
    * Rewrite confusing code instead of adding comments.
    * There should be a space after a comment start sequence.