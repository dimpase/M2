## Short introduction
### What is CMake
CMake is a meta-build system. Instead of running `./configure` and `make`, we use `cmake` and `ninja`

### Download
* Mac: `brew install cmake`
* Linux: use your package manager: `apt`, `dnf`, `pacman` etc
* For other needed tools, see [INSTALL-CMake.md](https://github.com/mahrud/M2/blob/feature/cmake/M2/INSTALL-CMake.md)

## Building Macaulay2 using CMake
0. Clone a Macaulay2 repository, e.g. `git clone https://github.com/Macaulay2/M2.git` or your own fork.
1. Add @mahrud's repository as a remote and checkout the cmake branch
```
git remote add mahrud https://github.com/mahrud/M2.git
git fetch mahrud
git checkout feature/cmake
```
**Note**: make sure the source directory does not contain any in-source build artifacts by running `make clean distclean` from the *source* directory. Note that this is cleaning artifacts from the `configure` build system.
2. Move to the build directory and run cmake
```
cd M2/M2/BUILD/build
cmake -GNinja -S../.. -B. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release
```
**Note**: If you're on a Mac, you might have to use
```
CC=/path/to/gcc CXX=/path/to/g++ cmake -GNinja -S../.. -B. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release
```
You can confirm the versions with `gcc --version`. Versions above 7 have been tested. There are known issues with `AppleClang`, so avoid that if possible.

3. Run `ninja build-libraries`. **This has to come first!**

4. Run `ninja M2-binary M2-core` to build the M2 executable and the core package

5. Run `ninja install-packages` to install all packages, and `ninja install` to install Macaulay2.

6. Run `ctest -R [keyword] -j4` to run the tests with the given keyword. Try `unit-tests`, `normal`, `check`, `check-Elimination`, or `check-Elimination-0`.

Other flags and build targets are available, see [INSTALL-CMake.md](https://github.com/mahrud/M2/blob/feature/cmake/M2/INSTALL-CMake.md) for details.

## Issues and solutions
### Givaro
**Issue:** `ninja` fails with an error `fatal error: givaro/modular-double.h: No such file or directory` even though the `givaro` package is installed.

**Solution:** run `ninja build-givaro` to force building `givaro`.


### `gmp_CCmutable`
**Issue:** `ninja` fails with an error `engine.h:84:3: error: ‘gmp_arrayZZ’ does not name a type; did you mean ‘gmp_newZZ’`.

**Solution:** run `make clean distclean` **from the source directory**. This cleans the build artifacts from an in-source build with the `configure` system.

## Additional info
* [Slides](https://www-users.math.umn.edu/~mahrud/journal/meeting/cmake/#/)
* [INSTALL-CMake.md](https://github.com/mahrud/M2/blob/feature/cmake/M2/INSTALL-CMake.md)

