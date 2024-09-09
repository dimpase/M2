# Quick start

After downloading the dependencies for your system (see below), do the following:

```
git clone https://github.com/Macaulay2/M2
cd M2/M2
make
cd BUILD
../configure --enable-download
make
sudo make install
```

*Note*:  On macOS and BSD systems, use `gmake` instead of `make`.

# Dependencies

Here are some dependencies you may have to install on your system to build Macaulay2:

## Arch Linux

```
sudo pacman -S 4ti2 autoconf automake bison boost cddlib coin-or-csdp eigen fflas-ffpack flex flint gc gcc gcc-fortran gfan git givaro glpk gtest icu libtool libxml2 lrs make mpfi nauty normaliz ntl onetbb patch pkgconf python singular texinfo time topcom which
```
*Note:*
- Add `--with-gtest-source-path=/usr/src/googletest` to the call to `configure` so that it can find GoogleTest.
- cohomCalg, Frobby, Mathic, Mathicgb, Memtailor, MPSolve, and Frobby are not available as packages on Arch Linux and will be downloaded and built.  Alternatively, Frobby is available in the [Arch User Repository](https://aur.archlinux.org/packages/frobby).

## Debian/Ubuntu

```
sudo apt install 4ti2 autoconf automake bison ca-certificates cohomcalg coinor-csdp fflas-ffpack flex g++ gfan gfortran git install-info libboost-dev libboost-regex-dev libboost-stacktrace-dev libcdd-dev libeigen3-dev libffi-dev libflint-dev libfrobby-dev libgc-dev libgdbm-dev libgivaro-dev libglpk-dev libgmp-dev libgtest-dev liblzma-dev libmathic-dev libmathicgb-dev libmemtailor-dev libmpfi-dev libmpfr-dev libmps-dev libnauty-dev libncurses-dev libnormaliz-dev libntl-dev libopenblas-dev libpython3-dev libreadline-dev libsingular-dev libtbb-dev libtool-bin libxml2-dev lrslib make nauty normaliz patch pkgconf python3 singular-data time topcom wget zlib1g-dev
```
*Note:*  
- On Ubuntu 18.04 (Bionic Beaver) and Ubuntu 20.04 (Focal Fossa) run the following first, as several of the above dependencies are missing from the official Ubuntu archives:
  ```
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:macaulay2/macaulay2
  ```

## Fedora

```
sudo dnf install 4ti2 TOPCOM autoconf automake bison boost-devel cddlib-devel cohomCalg csdp-tools diffutils eigen3-devel factory-devel fflas-ffpack-devel flex flint-devel g++ gc-devel gcc-gfortran gdbm-devel gfan git glpk-devel gmp-devel lapack-devel libffi-devel libfrobby-devel libnauty-devel libnormaliz-devel libtool libxml2-devel lrslib-utils make mathic-devel mathicgb-devel memtailor-devel mpfi-devel mpfr-devel mpsolve-devel nauty ncurses-devel normaliz ntl-devel patch python3-devel readline-devel tbb-devel which xz-devel zlib-devel
```
*Note:*
- Add `CPPFLAGS=-I/usr/include/frobby` to the call to `configure` so that it can find Frobby.
- Fedora's GoogleTest package does not include some necessary files, so it will be downloaded and built.
- In Fedora 41 and later, lrslib must be loaded as an environment module first:
  ```
  sudo dnf -y install environment-modules
  source /etc/profile.d/modules.sh
  module load lrslib-x86_64
  ```

## Gentoo
Coming soon

## macOS
Coming soon

## Red Hat Enterprise Linux

```
sudo dnf install autoconf automake bison boost-devel bzip2 diffutils eigen3 flex gc-devel gcc-c++ gcc-gfortran gdbm-devel git glpk-devel gmp-devel lapack-devel libffi-devel libtool libxml2-devel make mpfr-devel ncurses-devel openblas-devel patch python3-devel readline-devel tbb-devel which xz-devel zlib-devel
```
*Note:* You must have the [EPEL](https://docs.fedoraproject.org/en-US/epel/) enabled in order to install several of these packages.

## SUSE
Coming soon

# Getting the source code

The current development version of the source code can be obtained with this
command, assuming you have installed `git` on your machine:

    git clone https://github.com/Macaulay2/M2

A directory called `M2` which you can move or rename, will be created.  By default, the `master` branch
of the M2 repository will be checked out.

The `release` tags tend to be more stable, and if you compile from one of
those, you'll have the same functionality as those who download our binary
releases.  So, after cloning, you can switch to the tag containing version 1.24.05,
for example, with the following command:

    git checkout release-1.24.05

Instead of `release-1.24.05` you should, of course, use the most recent one.

The following command shows the list of release tags:

    git tag | grep release

However, if some time has passed since the most recent release and your system
has newer versions of some of Macaulay2's dependencies than were available at
the time of the release, you may have more success building the `master` branch.

The following commands, run from the top level of this source tree (the parent
of the directory this file is in) will download the latest changes to the
source code:

    git pull
    git submodule sync
    git submodule update

To obtain the latest, but potentially unstable, changes to the Macaulay2 source
code, switch to the `development` branch:

    git checkout development

# Configuring the build

After downloading the dependencies and cloning the git repository, the next step is to generate and run the configuration script.

First, change into the `M2` subdirectory of the repository (so `cd M2/M2` if you just cloned the repository) and run `make` (or `gmake` on macOS or BSD), which checks that a few programs are up-to-date, generates the `configure` script using [autoconf](https://www.gnu.org/software/autoconf/), and ensures that the [M2-emacs submodule](https://github.com/Macaulay2/M2-emacs) is updated.

Now run the following:

```
cd BUILD
../configure
```

You will likely need need to add one or more command-line options to `configure`.  For a complete list, run `../configure --help`.  We now outline several of the most important options.

## Enabling downloads

In most builds, several of the dependencies must be downloaded and built.  In order to download the source for these dependencies, add the option `--enable-download` to `configure`.

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

# Compiling Macaulay2

Now the directory to be in is the one containing this file in the source
distribution -- it is called "M2", and is a subdirectory of the top level
directory of the source tree.  If you are reading this file on the web, it may
be more convenient to switch now to reading it in its location in the source
tree.

Begin with this command:

        make

The "make" command above runs the commands "autoconf" and "autoheader", which
create the "configure" script and the "include/config.h.in" file, needed in the
next steps.  Once those files are created, it is not necessary to make them
again.  The "make" command on your system should be a recent version of GNU
make.

Now continue building the program this way:

        ./configure --enable-download --prefix=/foo/bar
        make
        make check                      # optional
        make install

Remember to add any options specified above, in the section for your particular
operating system, to the "configure" command line.

Files will then be installed in the following directories:

        /foo/bar/bin
        /foo/bar/share/Macaulay2
        /foo/bar/share/doc/Macaulay2
        /foo/bar/share/man/man1
        /foo/bar/share/emacs/site-lisp
        /foo/bar/lib/Macaulay2

The Macaulay2 program itself will be located at /foo/bar/bin/M2.

Choose an appropriate directory path, instead of /foo/bar, as the installation
prefix, or omit the option entirely for installation in /usr/local.

Note: the "make" program in the commands above should be at least version 4.
Under Mac OS X, one encounters an old version of "make", so it is better to use
the "gmake" program, as provided by "brew", and installed according to the
instructions above.

To take advantage of parallelism when running "make", append an option of
the form "-jN" to the command line, where "N" is replaced by the number of
processors you wish to devote to the task.  (Our makefiles are just beginning to
take advantage of this.)

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

To specify a different installation location for the "make install" command you
may add an option to the "make install" line, as follows:

        make install prefix=/foo/bar

To make an encapsulated directory tree or distribution tarball suitable for use
with the program "epkg" (see https://github.com/DanGrayson/epkg), add the option

        --enable-encap

to the "configure" command above.

The effect is to insert one more component into the path names used at
installation time, so that in response to 

        make prefix=/foo/bar install

files will be installed in the following directories:

        /foo/bar/Macaulay2-*/bin
        /foo/bar/Macaulay2-*/share/Macaulay2
        /foo/bar/Macaulay2-*/share/doc/Macaulay2
        /foo/bar/Macaulay2-*/share/man/man1
        /foo/bar/Macaulay2-*/share/emacs/site-lisp
        /foo/bar/Macaulay2-*/lib/Macaulay2

Each * above is replaced by the current version number.  There will
also be a few extra files placed in the directory /foo/bar/Macaulay2-*
which instruct epkg how to make appropriate symbolic links to install
our program, and how to initialize the dumped data file, if present:

        /foo/bar/Macaulay2-*/encapinfo
        /foo/bar/Macaulay2-*/postinstall
        /foo/bar/Macaulay2-*/preremove

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

# Unexpected problems

Suppose you encounter error messages like this one when compiling in libraries/mpir:

       tmp-mul_1.s:94: Error: no such instruction: `mulx (%rsi),%r9,%r8'

Then try adding --build=`./config/config.guess` to the command line of the
'configure' command.  This will tell mpir to build itself using just machine
instructions common to all the architectures in the same class as the
architecture of your machine, instead of optimizing itself for speed according
to your system.	 Mpir seems overconfident that the assembler on the machine
knows about all the machine instructions on the machine.