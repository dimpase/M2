### [[Using CMake|Building M2 from source using CMake]]

You can reduce the compilation time by installing dependencies from Homebrew when compiling Macaulay2 from source. From the top directory of the git repository, run:
```bash
brew tap macaulay2/tap
brew install ccache
brew install $(brew deps --1 --include-build macaulay2/tap/M2)

deps=$(brew deps --1 --include-optional macaulay2/tap/M2 | tr '\n' ';')
paths=$HOMEBREW_PREFIX/opt/${deps//;/;$HOMEBREW_PREFIX/opt/}

cd M2/BUILD/build
cmake -GNinja -S ../.. -B . \
      -DBUILD_NATIVE=OFF \
      -DCMAKE_PREFIX_PATH=$paths \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/usr

ninja
```
Also see this [Wiki](https://github.com/Macaulay2/homebrew-tap/wiki).

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