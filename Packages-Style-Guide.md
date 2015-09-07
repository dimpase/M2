**Please use this page to post style (and find out and use) conventions for writing packages in Macaulay 2.**

* General recommendations :
    * Any violation of the guide is allowed if it enhances readability.
    * The rules can be violated if there are strong personal objections against them.

* Naming conventions :
    * Names representing types must be nouns and written in mixed case starting with upper case.
    * Variable names must be in mixed case starting with lower case.
    * Names representing methods must be verbs and written in mixed case starting with lower case.
    * The prefix "is" should be used for Boolean variables and methods.
    * Abbreviations in names should be avoided.
    * Naming of optional arguments:
        * ```Verify``` : whether to check that a result is correct or well defined

* Use of types
    * Do not use an object of one type to "represent" an object of another.
         * Example: don't use a matrix to represent the submodule spanned by its columns.
    * Do not introduce a function that performs two consecutive operations, when it would be 
           clearer to factor it into a composite of two functions.  If necessary, introduce
           a new type to serve as the type of the intermediate result.

* Order of arguments:
    * Functions should take arguments in increasing order of complexity.  For example, if the 
      arguments are an integer and a module, put the integer first.
    * The argument upon which the function mainly acts should go last.

* Solutions to puzzles:
    * To get a user symbol, such as "x", use ```getSymbol "x"```.  To get n user variables starting with
      "a", use ```vars(0 ..< n)```.
    * To control the order of loading of imported packages ("PackageImports" option) and exported
      packages ("PackageExports" option) while the current package is being loaded, mention the exported
      packages in the list of imported packages, and juggle the sequence of imported packages.
 
* Behavior of code:
    * A package should set no variables in the User dictionary without an explicit request from
      the user.
        * The function "use" should never be used in a package.
        * To avoid setting user variables when creating a polynomial ring, use something like
          ```QQ(monoid[getSymbol "a"])``` instead of ```QQ[getSymbol "a"]```
    * Any names of variables in rings created by the package that get exposed to the user through
      returned values, directly or indirectly, should be accessible to the user.
      So use ```QQ(monoid[getSymbol "a"])``` or ```QQ(monoid[vars 0])``` instead of ```QQ[a]```.

* Miscellaneous :
    * The use of magic numbers in code should be avoided.
    * Packages should never export or protect single characters.
    * Variables must never have dual meaning.
    * Use of global variables should be minimized.
        * TODO : Discuss when to overload names.

* Layout :
    * The incompleteness of split lines must be made obvious: break after a comma, break after an
      operator.
    * Lazy evaluation :
    * TODO : Discuss error checking.

* White space :
    * Contents of regions delimited by parentheses, braces, or brackets that consist of multiple lines
      should be indented more than the surrounding lines, with the same indentation for every line.
    * Operators should be surrounded by a space character.
        * But ```n = n+1;``` doesn't look so bad, so maybe this should apply just to loose operators.
    * Commas should be followed by a white space.
        * But ```QQ[x,y,z]``` looks fine...
    * Semicolons should be followed by a space character.
    * Logical units within a block should be separated by one blank line.
    * Statements should be aligned.

* Documentation:
    * Each exported data type, method, and function must have a documentation page.  
    * Each documentation page must have an example.

* Comments :
    * Rewrite confusing code instead of adding comments.
    * There should be a space after a comment start sequence.
