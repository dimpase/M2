## Doxygen

It isn't complete, but it has some useful information.  Especially the class structure and inheritance.

## Branches

Differences between several current branches of M2 include memory allocation schemes (related to garbage collection issues).

## Unit tests

"ctest -R unit" does the tests labeled unit.  Alternately, gmake check (different format).  These are fast tests to check easy things.  Add a unit test by going into build directory e/unit-tests directory.  Write as a function with EXPECT_EQ(Expected,function call).  There are other checks, but this should be enough for most purposes.  TEST(Test suite name, specific test name).  Uses Google tests.