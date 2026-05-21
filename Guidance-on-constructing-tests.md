## Why test?

Tests are useful in your package for these reasons:

- If somebody changes something in the future which breaks your code, they will know and will be able to adjust the code so it doesn't.
- Tests compatibility with various versions of other packages (e.g. if you test against output of another package).
- It makes sure that your code is right (if you test with a known example from a textbook, for example).
- The code complains adequately if functions are fed wrong input.
- Recording errors in code so they do not happen again.

## Types of tests

- **Regression tests:** when there's an error, and you fix it, you put in a test to ensure it doesn't happen again in the future.
```macaulay2
  assert(det(M)!=0)
```

- **Type test:** does this function give the correct type.
```macaulay2
  assert(instance(foo(x),List))
```

- **Run test:** does the code run at all?
```macaulay2
  foo(x)
```

- **Error test:** if an error SHOULD occur on `foo(x)`, you can make sure that happens with:
```macaulay2
  assert(try (foo(x); false) else true)
```

- **Unit test:** just check that the output of something is something else.
```macaulay2
  assert(foo(x)==2)
```

- **Property test:** checks a property of a function on an example.
```macaulay2
  QQ[x,y]
  I = ideal(x^2, x*y)
  assert(isSubset(I, radical I))
```

## How to add tests to your M2 package

```macaulay2
--This is a comment, write what you'd like here, like "testing dimension and degree"
TEST ///
R = QQ[x,y,z]
assert(dim(ideal(x,y))==1)
assert(degree(ideal(x,y))==1)
///

--This is a second test now.
TEST ///
R = QQ[x,y,z]
assert(dim(ideal(x,y))==1)
///

--repeat these so that at least each exported function gets tested
```

## How tests work

- A test block will fail if there is any error in the block.
- Tests are implicitly numbered in the order in which they are read, starting at `mypackage.m2`.

## How to run tests

```macaulay2
check "SumsOfSquares"   -- runs all tests in the package SumsOfSquares
check_3 "SumsOfSquares" -- checks the third test in the SumsOfSquares package
                        -- capturing check(3, "SumsOfSquares")  -- .197867s elapsed
tests("SumsOfSquares")  -- gives each test, and where it is in the code base
      {0 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1221:5-1230:3] }
      {1 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1233:5-1247:3] }
      {2 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1250:5-1261:3] }
      {3 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1264:5-1271:3] }
      {4 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1274:5-1292:3] }
      {5 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1295:5-1302:3] }
      {6 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1305:5-1347:3] }
      {7 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1350:5-1374:3] }
      {8 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1377:5-1390:3] }
      {9 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1393:5-1427:3] }
      {10 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1430:5-1434:3]}
      {11 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1437:5-1442:3]}
      {12 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1445:5-1449:3]}
      {13 => TestInput[/usr/share/Macaulay2/SumsOfSquares.m2:1452:5-1456:3]}
```

## Where to put tests

Here are common places people choose to put tests:

- In the main package file `mypackage.m2`, either right after a function is defined, or all together at the end.
- A common choice is putting them all at the end of the top package file.
- The recommended choice (especially for new contributors) is in a directory:
```
  /packages/mypackage/tests.m2
```
  and load this file in `mypackage.m2`. Don't forget to set `AuxiliaryFiles=>true` in the preamble.

## General guidelines

- Each exported function should be tested with all options if options are available.
- Always test the trivial cases and boundary cases (what if you give the empty list? the zero ideal `<0>`? `<1>`?).
- Do not repeatedly construct the exact same object in one test block. You can use it more than once!
- Try to keep each test to a minimal time requirement (over 5s will be flagged and only allowed if necessary).
- Crucial core functions, give several tests, possibly right after defining the function.
- Sometimes `toString` is useful (or `value(toString(x))` if you are concerned about printing breaking things).
- Note: `=` means assignment, `==` checks that two things are mathematically the same, `===` are these the literal same object in the computer science sense:
```macaulay2
  i8 : R = QQ[x,y];
  i9 : ideal(x,y) === ideal(x+y,y)
  o9 = false
  i10 : ideal(x,y) == ideal(x+y,y)
  o10 = true
```
- Test properties, not just examples! e.g.:
```macaulay2
  I = ideal(x^2, x*y)
  assert(isSubset(I, radical I))
```
- Test bad input deliberately.
- Document why non-obvious tests exist (i.e. regression tests).
- In general, it's good to have comments on why you are testing certain things.