* General recommendations :
    * Strive for readability.
    * Use Unicode where appropriate, as in names of authors.

* Naming conventions :
    * Avoid acronyms in identifier names.
    * Prefer unabbreviated English words in identifier names.
    * Names representing types should be nouns and written in mixed case starting with upper case.
    * Names representing optional arguments should be capitalized.
    * Variable names must be in mixed case starting with lower case.
    * Names representing methods must be verbs and written in mixed case starting with lower case.
      They should not include the name of the type of object expected as argument, since the idea
      of such methods is that they are mathematical abstractions that act on a variety of types of
      mathematical object.
    * The prefix "is" should be used for Boolean variables and methods.  Examples:
         * `isPolynomialRing`, `isPrimary`, `isPrime`, `isPrimitive`
    * Abbreviations in exported names should be avoided.  Correct: "formalDepth".  Incorrect: "fD".
    * Naming of keys in hash tables:
        * Use existing symbols, when possible.  Examples:
             * `source` and `target`, as keys for the source and target of a map
    * Naming of optional arguments:
        * Names of optional arguments should be capitalized
        * Use existing names, when possible.  Examples:
            * `Verify` : whether to check that a result is correct or well defined
            * `Verbose` : whether to print extra information
    * Preserve the distinction between file names, such as `Foo.m2`, and package names, such as _Foo_.
      A package is an academic work, consisting possibly of multiple files.  Set package
      names in italic.

* Use of types
    * Do not use an object of one type to "represent" an object of another.
         * Example: don't use a matrix to represent the submodule spanned by its columns.
    * Do not introduce a function that performs two consecutive operations, when it would be 
           clearer to factor it into a composite of two functions.  If necessary, introduce
           a new type to serve as the type of the intermediate result.
    * It is usually a mistake to test whether the class of an object is equal to a certain class,
       because that disables inheritance.  In other words, instead of writing something like
       `class x === T`, write `instance(x,T)`.

* Use of optional arguments
    * A multiplicity of method functions that are simple variations of each other may
      indicate that simplification is possible if named optional arguments are used
      appropriately.

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
        * To determine whether your package sets User variables, use `listUserSymbols` after running some
          of the code in your package.
        * The function `use` should never be used in a package, unless the ring contains no user variables.
        * The function `vars` should not be used in a package.
        * To avoid setting user variables when creating a polynomial ring, use something like
          ```QQ(monoid[getSymbol "a"])``` instead of ```QQ[getSymbol "a"]```
    * Any names of variables in rings created by the package that get exposed to the user through
      returned values, directly or indirectly, should be accessible to the user.
      So use ```QQ(monoid[getSymbol "a"])``` or ```QQ(monoid[vars 0])``` instead of ```a := local a; QQ[a]```.

* Miscellaneous :
    * Avoid redundant parentheses.  Write `f x` instead of `f(x)`.
    * When a function should return more than one thing, package the several things
      in a sequence rather than in a list, because then the results can be assigned directly
      to several variables with something like `(a,b,c) = f(x,y,z)`.
    * Don't test a Boolean value for equality with `true` or `false`, because `x===true` is equivalent
      to `x` and `x===false` is equivalent to `not x`.
    * Avoid the use of `return`, especially on the last line of a function.
    * The use of magic numbers in code should be avoided.
    * Packages should never export or protect identifiers whose names consist of a single character.
    * Variables must never have dual meaning.
    * Use of global variables should be minimized.
    * Many things you'll be tempted to type more than once have abbreviations.  For example,
      when R is a ring, then `first entries vars R` can be shortened to `gens R`.
    * Don't use braces `{ ... ; ... ; ... }` for blocks of code where you don't intend to make a list.
      Instead, write `( ... ; ... ; ... )`.

* Layout :
    * The incompleteness of split lines must be made obvious: break after a comma, break after an
      operator.
    * If you use a text editor where TAB stops are set to something other than every 8th location on
      the line, then don't use TABs at all for indentation, as your users will see odd-looking
      indentation.

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
    * **Choice of examples:** choose examples that illustrate usage sufficiently, without
      consuming excessive CPU time.  Assertions about the speed of your package can
      simply be written, and will be believed.
    * **Choice of tests:** package functionality should be adequately tested, without consuming excessive CPU time
      and memory.  (Limits are imposed, but under Mac OS X, they aren't enforced.)
    * Document the type of the return value of method functions, so the documentation generator
      can include those methods in the documentation of the type of the return value.
         * Example: ```resolution Module := ChainComplex => o -> (M) -> (...)```
    * Don't put blocks of example code adjacent to each other.  Merge them, or add some 
      text between them.
    * The "usage" forms for functions don't need to be in the form of assignment statements.
    * The "headline" of a documentation node should be a single brief phrase (not a complete sentence) and thus can be vague.  It should not
      refer to variables by name, because it can appear in a menu, without the accompanying
      body of the documentation node.
    * In the "Outputs" section, provide multiple entries only if the function returns a sequence with
      several entries in it.
    * In the "Outputs" section, state, for each output value, not only its
      type, but what it is.  For example, say that "resolution M" returns a
      free resolution of M.  Here you should give a mathematical description of
      the returned object.  It could be vague, clarified in the subsequent
      description, but it should be complete.
    * In the "Outputs" and "Usage" sections, there is no reason to assign the value returned by
      the sample code to a variable -- when there is just one output, there is no ambiguity.
    * Do not reload the current package in example code, because its source code might
      not be on the path of the user installing it.
    * Start each sentence with an English word, not an identifier or a symbol.
    * End each sentence with a period or question mark, not with a colon.  To indicate that
      example code just below is relevant, use English words, not a colon.
    * Don't use _Macaulay2_ identifiers as English words.  Learn how to use "ofClass" in this connection,
      so the English word and a hyperlink can be generated from the identifier.
    * Don't capitalize English words such as "list" or "tally", even though there are classes in
      _Macaulay2_ whose names are "List" and "Tally", unless you intend to refer to those classes.
      Examples of correct usage: "The function returns a list."  "The function returns an object
      of class List."  An example of incorrect usage: "The function returns a List."
    * Check the spelling of English words.
    * Read the documentation in a browser (see "viewHelp") to make sure it looks elegant.
    * All sentences should have verbs and subjects.
    * "different"
      * Don't use "different" gratuitously.  For example, "different matrices" is 
        no more informative than "matrices".
      * Don't use "different" when you mean "various" or "diverse".
      * Don't use the construction "different than" or "different to".  Use "different from" instead.
      * Don't use the construction "a different X than Y".  Say "an X different from Y".
    * Add a comma when starting a sentence with an adverb such as "Finally".
    * Use "if" as a prelude to "then", but use "whether" (and not "whether or not") to introduce a
      proposition.  Example: prefer "determine whether R is reduced" to "determine if R is reduced".
    * Use standard English punctuation.  In particular, each use of "e.g.", "i.e.", or "resp." should
      be followed by a comma.
    * Set names of software packages, such as _Macaulay2_, in italic.
    * Don't misplace the word "only".  Correct: "Fly only in the absence of fog."  Incorrect: "Only fly 
      in the absence of fog," for it implies not _driving_ in the absence of fog.

* Comments :
    * Delete commented-out code.
    * Rewrite confusing code instead of adding comments.
    * There should be a space after a comment start sequence.

* When submitting for publication or for inclusion in _Macaulay2_:
    * The `Headline` option to "newPackage" should be a brief phrase stating the topic of the package.  For example,
      the headline for the package "Tropical" is the phrase "tropical geometry".  It would be redundant to say something
      such as "a package for tropical geometry", "computations in tropical geometry", or "a package for computations in tropical geometry".
    * Remove any option `DebuggingMode => true` or `Reload => true` to "newPackage".  Your users
      aren't prepared to debug your package.
