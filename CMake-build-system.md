## Short introduction
### What is CMake
CMake is a meta-build system. Instead of running `/.configure` and `make`, we use `cmake` and `ninja`

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

2. Move to the build directory and run cmake
```
cd M2/M2/build/build
cmake -GNinja -S../.. -B. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release
```
_Note_ If you're on a Mac, you might have to use
```
CC=/path/to/gcc CXX=/path/to/g++ cmake -GNinja -S../.. -B. -DCMAKE_INSTALL_PREFIX=/usr -DCMAKE_BUILD_TYPE=Release
```

3. Run `ninja build-libraries`. **This has to come first!**

4. Run `ninja M2-binary M2-core` to build the M2 executable and the core package

5. Run `ninja install-packages` to install all packages, and `ninja install` to install Macaulay2.

Other flags and build targets are available, see [INSTALL-CMake.md](https://github.com/mahrud/M2/blob/feature/cmake/M2/INSTALL-CMake.md) for details.

## Additional info
* [Slides](https://www-users.math.umn.edu/~mahrud/journal/meeting/cmake/#/)
* [INSTALL-CMake.md](https://github.com/mahrud/M2/blob/feature/cmake/M2/INSTALL-CMake.md)
