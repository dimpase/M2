## Short introduction
### What is CMake
CMake is a meta-build system. Instead of running `/.configure` and `make`, we use `cmake` and `ninja`

### Download
* Mac: `brew install cmake`
* Linux: use your package manager: `apt`, `dnf`, `pacman` etc
* For other needed tools, see [INSTALL-CMake.md](https://github.com/mahrud/M2/blob/feature/cmake/M2/INSTALL-CMake.md)

## Building Macaulay2 using CMake
0. Clone a Macaulay2 repository, e.g. `git clone https://github.com/Macaulay2/M2.git` or your own fork.
1. Add @mahrud's repository as a remote `git remote add mahrud https://github.com/mahrud/M2.git
2. Fetch changes `git fetch mahrud`
3. Checkout the cmake branch `git checkout feature/cmake`