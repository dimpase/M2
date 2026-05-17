# Quick start

After downloading the dependencies for your system (see below), do the following:

```
git clone https://github.com/Macaulay2/M2
cd M2/M2/BUILD/build
../../autogen.sh
../../configure
make
sudo make install
```

*Note*:  On macOS and BSD systems, use `gmake` instead of `make`.

# Dependencies

Here are some dependencies you may have to install on your system to build Macaulay2:

## Arch Linux

```
sudo pacman -S 4ti2 autoconf automake bison boost boost-libs cddlib coin-or-csdp eigen fflas-ffpack flex flint gc gcc gcc-fortran gfan git givaro glpk gtest icu jansson libtool libxml2 lrs make mpfi nauty normaliz ntl onetbb openblas patch pkgconf python singular texinfo time topcom which
```
*Note:*
- cohomCalg, Frobby, Mathic, Mathicgb, Memtailor, and MPSolve are not available as packages on Arch Linux and will be downloaded and built.  Alternatively, Frobby is available in the [Arch User Repository](https://aur.archlinux.org/packages/frobby).

## Debian/Ubuntu

```
sudo apt install 4ti2 autoconf automake bison ca-certificates cohomcalg coinor-csdp fflas-ffpack flex g++ gfan gfortran git install-info libboost-dev libboost-regex-dev libboost-stacktrace-dev libcdd-dev libeigen3-dev libffi-dev libflint-dev libfplll-dev libfrobby-dev libgc-dev libgdbm-dev libgivaro-dev libglpk-dev libgmp-dev libgtest-dev libjansson-dev liblzma-dev libmathic-dev libmathicgb-dev libmemtailor-dev libmpfi-dev libmpfr-dev libmps-dev libnauty-dev libncurses-dev libnormaliz-dev libntl-dev libopenblas-dev libpython3-dev libreadline-dev libsingular-dev libtbb-dev libtool-bin libxml2-dev lrslib make msolve nauty normaliz patch pkgconf python3 singular-data time topcom wget zlib1g-dev
```

## Fedora

```
sudo dnf install 4ti2 TOPCOM autoconf automake bison boost-devel cddlib-devel cohomCalg csdp-tools diffutils eigen3-devel factory-devel fflas-ffpack-devel flex flint-devel g++ gc-devel gcc-gfortran gdbm-devel gfan git glpk-devel gmp-devel gtest-devel jansson-devel lapack-devel libffi-devel libfrobby-devel libnauty-devel libnormaliz-devel libtool libxml2-devel lrslib-utils make mathic-devel mathicgb-devel memtailor-devel mpfi-devel mpfr-devel mpsolve-devel msolve nauty ncurses-devel normaliz ntl-devel patch python3-devel readline-devel tbb-devel which xz-devel zlib-devel
```
*Note:*
- In Fedora 41 and later, lrslib should be loaded as an environment module:
  ```
  sudo dnf -y install environment-modules
  source /etc/profile.d/modules.sh
  module load lrslib-x86_64
  ```

## macOS

Most dependencies require first installing [Homebrew](https://brew.sh/).

```
brew install autoconf automake gnu-tar make texinfo libomp bdw-gc cddlib googletest
brew install --only-dependencies Macaulay2/tap/M2
brew install Macaulay2/tap/memtailor Macaulay2/tap/mathic Macaulay2/tap/mathicgb
```

*Note:*
- Add the following options to the call to `configure` so that it can find some of these dependencies:
  ```
  LDFLAGS="-L$(brew --prefix)/lib -L$(brew --prefix factory)/lib -L$(brew --prefix libomp)/lib \
      -L$(brew --prefix readline)/lib -L/Library/Frameworks/Python.framework/Versions/3.13/lib" \
  CPPFLAGS="-I$(brew --prefix)/include -I$(brew --prefix)/include/cddlib -I$(brew --prefix factory)/include \
      -I$(brew --prefix libomp)/include -I$(brew --prefix readline)/include" \
  F77="gfortran-14" \
  PKG_CONFIG_PATH="$(brew --prefix factory)/lib/pkgconfig"
  ```
  Replace the Python and gfortran version numbers with the ones appropriate for your system.

## Red Hat Enterprise Linux

```
sudo dnf install autoconf automake bison boost-devel bzip2 diffutils flex flexiblas-devel gcc-c++ gcc-gfortran git gmp-devel info jansson-devel libffi-devel libtool libxml2-devel make mpfr-devel ncurses-devel patch python3-devel readline-devel tbb-devel which xz-devel zlib-devel
```
Remove `flexiblas-devel` if you are on RHEL 8.

If you have the [EPEL](https://docs.fedoraproject.org/en-US/epel/) enabled, then also install the following:
```
sudo dnf install eigen3 gc-devel gdbm-devel glpk-devel gtest-devel jansson-devel
```

If you do not have EPEL enabled, then either install [Jansson](https://github.com/akheron/jansson) manually or build Macaulay2 without Jansson support by passing `--without-jansson` to `configure`.


## OpenSUSE Tumbleweed

```
sudo zypper install 4ti2 autoconf automake bison boost-devel bzip2 cddlib-devel cmake diffutils e-antic-devel eigen3-devel fflas-ffpack-devel flex flint-devel gawk gc-devel gcc gcc-c++ gcc-fortran gdbm-devel gfan git givaro-devel glpk-devel gmp-devel gtest libboost_regex-devel libboost_stacktrace-devel libfactory-devel libfactory-gftables libffi-devel libjansson libtool libxml2-devel lrslib make mpfi-devel mpfr-devel nauty ncurses-devel normaliz normaliz-devel ntl-devel openblas-devel patch pkgconf python3-devel tbb-devel which xz-devel zlib-devel
```

## Gentoo
Coming soon

# Getting the source code

The current development version of the source code can be obtained with this
command, assuming you have installed `git` on your machine:

    git clone https://github.com/Macaulay2/M2

A directory called `M2` which you can move or rename, will be created.  By default, the `stable` branch
of the M2 repository will be checked out.

To obtain the latest, but potentially unstable, changes to the Macaulay2 source
code, switch to the `development` branch:

    git checkout development

Alternatively, you may download a source tarball from the Macaulay2 website: https://macaulay2.com/Downloads/SourceCode/.  After downloading, unpack it:

    tar -xvf Macaulay2-1.25.11.tar.gz

Replace the version number as appropriate.

# Configuring the build

After downloading the dependencies and cloning the git repository, the next step is to generate and run the configuration script.  The `autogen.sh` script generates the `configure` script using [autoconf](https://www.gnu.org/software/autoconf/) and ensures that the [M2-emacs submodule](https://github.com/Macaulay2/M2-emacs) is updated.

```
cd M2/M2/BUILD/build
../../autogen.sh
```

Note that this step is unnecessary when using a source tarball, as the `configure` script and Emacs files are included.

Now run the following:

```
../../configure
```

You will likely need need to add one or more command-line options to `configure`.  For a complete list, run `../../configure --help`.  We now outline several of the most important options.

## Configuring the documentation

The longest step in building Macaulay2 is generating all of the examples for the documentation.  By default, documentation is generated in html format, info format, and in database files used by the Macaulay2 `help` command.  Optionally, pdf documentation may be generated.  You can configure this behavior using the `--enable-documentation` option.

It can take a space-delimited list containing any of `html`, `info`, or `pdf`, e.g., `--enable-documentation="html pdf"` will generate the html and pdf documentation, but not the info documentation.

The database files are always generated, expect in the following cases:

* `--disable-documentation`: No examples are generated.  This is highly discouraged, as the `help` command will be slowed down considerably since documentation will be generated on the fly.
* `--enable-documentation=download`:  No examples are generated, but html, info, and database documentation are downloaded from the Macaulay2 website.  This option will only work for stable releases.

## Disabling downloads

In many builds, several of the dependencies must be downloaded and built.  To disable this feature, add the option `--disable-download` to `configure`.

## Building with Python support

The `Python` package embeds a Python interpreter inside Macaulay2.  For this
to work, the Macaulay2 binary needs to be linked against the Python shared
library.  To do this, add the option `--with-python` to `configure`.  Optionally, you may specify the Python version, e.g.,
`--with-python=3.12`.  Otherwise, the system's default version is used.

Make sure that Python header files and shared library are available on your
system.  If the Python shared library is not in a standard location, then add its path
to `LDFLAGS`.  For example, if Python has been installed using brew, then add
the following to `LDFLAGS`, replacing `X` with the appropriate minor version:
`-L$(brew --prefix python)/Frameworks/Python.framework/Versions/3.X/lib`.

## Building without libffi support

Use of the `ForeignFunctions` package requires linking the Macaulay2 binary
against [libffi](https://sourceware.org/libffi/).  This has been known to
cause issues on some machines, and so it is possible to opt out of
this feature by adding the `--without-libffi` option to `configure`.

To enable the running of the NTL "wizard", which conducts time consuming
experiments to optimize the speed of its code, before compiling it, add the
option --enable-ntl-wizard to the "configure" command line above.

To use a different prefix, say $HOME/local, for finding libraries and include
files installed in a nonstandard location, add the following options to the
"configure" command line:
        LDFLAGS="-L$HOME/local/lib" CPPFLAGS="-I$HOME/local/include"
That step is unnecessary if the compiler was compiled from sources and installed
with that prefix.

To use a different compiler suite, such as gcc version 4.8.2 as compiled above,
add something like the following to the "configure" command line:
        CC=gcc-4.8.2 CXX=g++-4.8.2 FC=gfortran-4.8.2
That step is unnecessary if the environment variables CC and CXX are set as
described above.

To specify libraries to link against during configuration, use the LIBS
environment variable, as described in documentation for autoconf.  For example,
to link with libfoo, add the following option to the "configure" command line:

        LIBS=-lfoo

To see descriptions of all the environment variables that influence
configuration, run this command and look at the section of the output
entitled "Some influential environment variables":

        ./configure --help

The only one of these variables with a nonempty default value is
CFLAGS, and its default value is "-g -O2".  That will be supplanted if
you override it.

# Compiling Macaulay2

After configuring Macaulay2, the next step is to run `make` from the same directory that you ran `configure`.  This should be GNU make, so if you are on a macOS or *BSD system, then use `gmake` instead.

```
make
sudo make install
```

To take advantage of parallelism when running "make", append an option of
the form "-jN" to the command line, where "N" is replaced by the number of
processors you wish to devote to the task.  (Our makefiles are just beginning to
take advantage of this.)


To specify a different installation location for the "make install" command you
may add an option to the "make install" line, as follows:

        make install prefix=/foo/bar

# Compiling for multiple machine architectures

By default, Macaulay2 will compile in such a way that it is adapted to the
architectural features of the CPU being used to do the compilation.  This is
especially true for the library mpir, which exploits many of the advanced
features of your CPU, determining them by running a small program and uses the
output from that to determine which optimization options (of the form
'-mtune=*' and '-march=*') to pass to gcc.

If you expect the Macaulay2 binary you build to run on other machines (for
example, if you are making a binary distribution to hand to others), then you
must prevent that from happening.

One way to do that is to pass an explicit "build target" to the configure
script, as in this example under Mac OS X:

   ./configure --build=x86_64-apple-darwin

The build target will be provided to the configure scripts of the libraries
needed, and, at least in the case of the mpir library, will prevent it from
optimizing further.

To find a suitable target, run :

   config/config.guess

To combine those two steps, run :

   ./configure --build=`config/config.guess`

# HTML validation

To validate all our HTML files, run:

   make validate-html

This depends on the installation of the validator (the Python utility
html5validator, available using pip), so we don't run it automatically.

# Rerunning the package examples

Some packages cache their example output in the source code tree, since they
depend on the presence of external programs not included with Macaulay2.  Here
we briefly summarize them and the software they depend on:

    gfanInterface StatePolytope need polymake, builds OK
	    http://polymake.org/lib/exe/fetch.php/download/polymake-2.13-1.tar.bz2
	    (Make 3.81 has a problem with their makefile, so use 4.0)
	    Polymake can be installed under Ubuntu with the following command:
 	         sudo apt-get install polymake

    Bertini needs bertini:
	    http://www.nd.edu/~sommese/bertini/
	which needs gmp and mpfr:
	    https://gmplib.org/
	    http://www.mpfr.org/

    PHCpack needs PHCpack, download the binary:
            http://homepages.math.uic.edu/~jan/download.html

    AdjointIdeal ConvexInterface MapleInterface Parametrization need Maple.

    ConvexInterface also needs the maple package "convex" installed.  See the 
    package documentation for hints about installing it.
    	    http://www.math.uwo.ca/~mfranz/convex/files/current/convex.m

# Warning messages

	-  warning: -jN forced in submake: disabling jobserver mode

	   This message can be ignored, if the previous recursive make command
	   had -j1 as an option, as -j1 implies the use of just one processor,
	   anyway.  (We use -j1 as an option when compiling third party libraries
	   whose makefiles are not known to support parallelism.)

# Autoconf, autoreconf, libtool, ...

If you get any mysterious error messages involving autoconf, autoreconf,
libtool, etc., try running

	 make -f Makefile get-tools

in the top level.  This command will install versions of those tools known to
work with Macaulay2.

# macOS Instructions

Here's how I've installed M2 from a Macports install on an M1 chip. Some of these steps might be specific to my setup. These instructions are for v1.21, and there are possible differences in the most recent version.

0) Download the M2 source from GitHub

1) Install Macports and install the libraries needed for M2 (as found in install instructions/make file). I forget which ones I actually installed. Make sure to install gcc or clang through Macports since Mac's built-in clang doesn't interface with libomp. Some of these libraries have different names than expected so "port search" is sometimes helpful to find the libraries.

2) Run gmake get-tools and then gmake . Sometimes the git command at this point needs to be run directly.

3) From the build directory, I use the following configure command: ../../configure --enable-download --enable-build-libraries=readline CC=/opt/local/bin/clang CXX=/opt/local/bin/clang++ CPPFLAGS="-I/opt/local/include -I/opt/local/include/tbb -I/opt/local/include/libomp" LDFLAGS="-L/opt/local/lib". Then, gmake as normal.

5) Csdp sometimes fails to compile. The problem is that -std=gnu17 (or similar) is missing from some of the compile commands. You need to add -std=gnu17 to the displayed compile command, something like "/opt/local/bin/clang -fopenmp -ansi -Wall -DUSEOPENMP -DSETNUMTHREADS -DUSESIGTERM -DUSEGETTIME -I../include -c -o op_o.o op_o.c -std=gnu17". The Csdp command may fail twice, then gmake should continue as normal.

6) Givaro sometimes fails to install. It tries to get the wrong version (4.1.1 and not 4.2.0). Go to <build_directory>/libraries/givaro and change the make file to have version 4.2.0 and URL=https://github.com/linbox-team/givaro/releases/download/v4.2.0/. Then run gmake, then go to build/givaro-4.2.0 and gmake and gmake install. Now, gmake should continue as normal.

7) For some reason, the files in the d directory are compiled out of order for me. Go to the <build_directory>/Macaulay2/d and run commands like ../c/scc1 -dep ../../../../Macaulay2/d/arithmetic.d and mv arithmetic.sig.tmp arithmetic.sig && mv arithmetic.dep.tmp arithmetic.dep
The order should be arithmetic, atomic, M2, system, strings, varstrin, strings1, errio, vararray, ctype, nets, varnets, interrupts, pthread0, stdiop0, gmp, engine, xml, stdio0, parse, expr, stdio, stdiop, err, gmp1, tokens, getline, lex, parser, binding, basic, convertr, common, util, struct, classes, buckets, equality, hashtables, regex, evaluate, sets, mysqldummy, pthread, actors, actors2, actors3, actors4, xmlactors, actors5, actors6, threads, interface, interface2, texmacs, boostmath, ffi, interp, version

8) The Bertini package sometimes fails to install. In the Bertini package, the bertiniRefineSols example is broken. Remove the bertiniRefineSols line in the example and replace it with S = sols.

9) Sometimes other packages, such as foreign functions need to be removed from the =distributedpackages list in the source package directory

10) In the development branch, make sure to disable Valgrind. Valgrind doesn't work on mac M1 chips and perhaps not the newest operating system. Remove functions in <top_directory>/Macaulay2/d/M2mem.c and M2mem.h that involve OrigFn.