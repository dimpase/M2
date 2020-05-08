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