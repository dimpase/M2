Work in progress. Contributors: Tim Duff, (your-name-here)

## Minimal setup 

1. [fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) [Macaulay2](https://github.com/Macaulay2/M2)
2. git [clone](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository) yourfork
3. Install [emacs](https://www.gnu.org/software/emacs/download.html)

Step 1 is perhaps optional if you don't intend to submit a [pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request). 

## Contents of source directory [M2/M2/](https://github.com/Macaulay2/M2/tree/master/M2)
* [README](https://github.com/Macaulay2/M2/blob/master/M2/README): generally a good place to start
* [BUILD](https://github.com/Macaulay2/M2/tree/master/M2/BUILD) directory: "This directory may be used as a convenient location for the build directory
trees."
* [INSTALL](https://github.com/Macaulay2/M2/blob/master/M2/INSTALL) & [INSTALL.mac](https://github.com/Macaulay2/M2/blob/master/M2/INSTALL.mac): Instructions. See OS-specific cheatsheets (to be written.)
* Macaulay2 directory: contains most of Macaulay2 itself, w/ important subdirectories
  * [e](https://github.com/Macaulay2/M2/tree/master/M2/Macaulay2/e): the engine (C++ language)
  * [d](https://github.com/Macaulay2/M2/tree/master/M2/Macaulay2/d): the interpreter (D language)
  * [m2](https://github.com/Macaulay2/M2/tree/master/M2/Macaulay2/m2): the top level core (Macaulay2 language)
  * [packages](https://github.com/Macaulay2/M2/tree/master/M2/Macaulay2/packages): where most users' code goes
  * also [c](https://github.com/Macaulay2/M2/tree/master/M2/Macaulay2/c) directory: C code obtained from D code is placed here
* [configure.ac](https://github.com/Macaulay2/M2/blob/master/M2/configure.ac): autoconf script that generates actual configure file
* distributions:
1. deb -> ubuntu, debian
2. dmg -> Mac
3. freebsd
4. other OS? tar file
* libraries
  * obtained from tar files
  * eg 4ti2, gfan
  * each directory contains instructions for how to build
* submodules
  * like "libraries", but obtained from git
# building from source w/ autotools
GNU paradigm: configure, then make. In this example, build directory is M2/M2/BUILD/cleveland
```
cd M2/M2/
make
./configure -h
mkdir BUILD/cleveland
cd BUILD/cleveland
../../configure --enable-download
make
```
Tips
* potentially helpful make flags 
  * -jn : use n threads
  * -C dir : recompile only in dir
* there are OS-specific additional instructions
  * for instance, set FC = gfortran for Debian systems
* configure options
  * some standard (like --help)
  * some less standard (--disable-gfan)

Things configure does:
* output: version, environment variables, OS, many checks
* checks for libraries (eg. mpir) and builds if not there / not right version. tricky. cMake improvements?
* starts to create files needed for make
* transformation: eg. foo.in -> foo. replaces identifiers (@PACKAGE_NAME) with their system-specific values
* can define macros w/ autoconf
  * AC_DEFUN. some other way?
  * arguments need square brackets
  -- final part created by AC_OUTPUT
## didn't cover
* how to use make
* anything else?

Quick links: [INSTALL](https://github.com/Macaulay2/M2/blob/master/M2/INSTALL) [Downloads](http://www2.macaulay2.com/Macaulay2/Downloads/) [["M2-internals"-notes]]