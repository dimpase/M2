### [[Using CMake|Building M2 from source using CMake]]

If Macaulay2 is bottled on Homebrew for your platform, you can reduce the compilation time by installing dependencies from Homebrew when compiling Macaulay2 from source.
```bash
brew tap Macaulay2/tap
brew trust Macaulay2/tap
brew install ccache $(brew deps --1 --include-build macaulay2/tap/M2)

OPT_PREFIX=$(brew deps --1 --include-build macaulay2/tap/M2 | \
	cut -d'/' -f-1 | sed "s|^|$HOMEBREW_PREFIX/opt/|" | paste -sd';' -)
```
Then, from the top directory of the git repository, run:
```bash
cd M2/BUILD/build
cmake -GNinja -S ../.. -B . \
      -DBUILD_NATIVE=OFF \
      -DCMAKE_PREFIX_PATH=$OPT_PREFIX \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/usr

ninja M2-core
```
Also see the full [[CMake guide|Building M2 from source using CMake]] and this [wiki](https://github.com/Macaulay2/homebrew-tap/wiki/).

### [[Using Autotools|Building M2 from source using Autotools]]

From the top directory of the git repository, run:
```bash
brew install ccache ctags gnu-tar make wget yasm

cd M2
gmake get-libtool
gmake -f Makefile

cd BUILD/build
CC=/usr/bin/gcc CXX=/usr/bin/g++ ../../configure \
    --enable-download \
    --enable-build-libraries="readline"

gmake IgnoreExampleErrors=false
```