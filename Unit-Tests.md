Work in progress. Contributors: Michael Burr, Anton Leykin, (your-name-here)

## Unit tests

The unit tests are fast tests that check easy things.  These tests use the Google test suite.  A new unit test can be created by going into the build directory e/unit-tests directory and writing a function with the command TEST(&lt;Test suite name&gt;,&lt;specific test name&gt;).  Within these tests, use EXPECT_EQ(&lt;Expected&gt;,&lt;function call&gt;) to check the value.  There are other tests, but this function should be enough for most purposes.

Run unit tests: Depending on the build method, there are different ways to run the tests depending on how M2 has been built.

1. Using the configure approach, run "make check".

2. Using the cmake approach, run "ctest -R unit"