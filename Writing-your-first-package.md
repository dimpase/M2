Creating a package is the most common way of contributing to Macaulay2. Packages come in many forms: they can contain code for working with objects of a certain category, help generate examples for testing a conjecture, or can be an implementation of algorithms introduced in the literature. Putting your code into a package makes it easier to share with other people, and also easier to maintain yourself.

## First steps

1. Download the "FirstPackage" package from [LINK]. This is a directory containing a test. Install it on your M2 system using the command `installPackage("FirstPackage")`. Look at the help using the command `viewHelp FirstPackage`.
2. Do some sample edits to the package and see what happens.
3. Have a look at the source code of some other M2 packages. You can find these on GitHub [here](https://github.com/Macaulay2/M2/tree/development/M2/Macaulay2/packages). Click on any file ending in `.m2` to see the code.
4. Download the package template from [LINK]. This is a directory containing a text file `PackageName.m2`, and a directory `PackageName`, which contains `Documentation.m2` and `Tests.m2`. These are all text files that you can edit in your favorite editor. Replace `PackageName` in both places by the name of your package (following the convention that every word starts with a capital letter). You are now ready to start writing your package!

## Writing your package

The package code has four parts:

1. The **preamble**, which starts with the `newPackage()` command and collects the metadata for your package.
2. The **main code** of the package.
3. The **documentation** of the package.
4. The **tests** of the package.

### The preamble

The preamble consists of two main commands: `newPackage()` and `export`.

Fill in the fields in the version of `newPackage` provided in the template. Details about the fields can be found in the [documentation](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_new__Package.html) for `newPackage()`. For any fields you are unsure about, it is safe to accept the default for now.

You will add the functions that you want your user to be able to access to the export list. This is a list of strings separated by commas, e.g.:

```macaulay2
export { "firstFunction", "secondFunction" }
```

### The main code of the package

This is the core of your package! See the [style guide](https://github.com/Macaulay2/M2/wiki/Package-Writing-Style-Guide) for conventions when writing M2 code. Try to make your code easy to read by other people and self-documenting - for example, `spairCount` is a better name for the number of S-pairs in your Gröbner basis calculator than `s`! When you have written some code, type `installPackage "YourPackageName"` to install your package.  You can then try to run the code.

### The documentation of the package

Edit the `Documentation.m2` file to add documentation to your package. Documentation is written in a structured format called "SimpleDoc". The first line is `beginDocumentation()`, followed by a sequence of "documentation nodes" that start with the word `doc`. The first (and most important) one is the documentation for the package as a whole. Some advice on how to structure this page can be found here[LINK]. It can be helpful to look again at some examples of real packages (see step 3 of the First Steps).

More information about writing documentation is available [here](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_writing_spdocumentation.html). The documentation for a documentation node is [here](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/SimpleDoc/html/_doc.html).

Once you have written some documentation nodes, reinstall your package and type `viewHelp YourPackageName`. This will bring up a webpage with your documentation displayed in the Macaulay2 format. To reinstall the package, you may first need to run:

```macaulay2
uninstallPackage("YourPackageName")
installPackage("YourPackageName", RemakeAllDocumentation => true)
```

### The tests of the package

Edit the `Tests.m2` file to add tests to your package. Make sure that all major mathematical parts of your package are tested, including edge cases. More guidance on how to construct tests is available here[LINK]. To check that the tests all run, type `check YourPackageName`.

## Distributing your package

Once your code is working, all tests pass, and the documentation is understandable by someone else, you will hopefully want to share it with other people. To get it distributed with Macaulay2, follow the instructions at [LINK].