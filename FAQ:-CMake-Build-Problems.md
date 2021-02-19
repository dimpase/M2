Below are a list of common issues and errors related to the CMake build. See the [install guide](https://github.com/Macaulay2/M2/blob/master/M2/INSTALL-CMake.md) for instructions on how to build Macaulay2 using CMake. If you run into a problem not listed below or among the list of issues labeled with [build system](https://github.com/Macaulay2/M2/labels/build%20system), please open a [new issue](https://github.com/Macaulay2/M2/issues/new).

<details>
<summary>Installing dependencies using Linuxbrew</summary>

On macOS CMake automatically finds libraries installed on the Homebrew prefix. In order to use Linuxbrew (which has the same interface and packages), use the following command to tell CMake to look under the right prefix:
```
cmake -DCMAKE_SYSTEM_PREFIX_PATH=`brew --prefix` .
```
</details>

<details>
<summary><code>/usr/include/c++/10.1.0/bits/unique_ptr.h:594:9: error: no matching function for call to std::__uniq_ptr_data</code> when using GCC 10 or Clang 10</summary>

This issue is due to an old version of FFLAS_FFPACK or Givaro libraries inserting an unnecessary `-fabi-version=6` flag to the compile command. Use the following command to tell CMake to build those libraries:
```
cmake -DBUILD_LIBRARIES="Givaro;FFLAS_FFPACK" .
```
</details>

<details>
<summary><code>/usr/include/boost/regex/v4/cpp_regex_traits.hpp:966: undefined reference to `boost::re_detail_107100::cpp_regex_traits_implementation<char>::transform_primary(char const*, char const*) const'</code></summary>

Same as above.
</details>

<details>
<summary><code>collect2: error: ld returned 1 exit status</code> on WSL2</summary>

This issue is likely due to a memory exhaustion bug in WSL2. Try cleaning the build artifacts and building with parallelization disabled:
```
ninja clean
ninja M2-core -j1
```
</details>

<details>
<summary><code>undefined reference to cblas_dgemm</code> on Arch Linux</summary>
The default OpenBLAS package on Arch Linux does not include function declarations for LAPACK and CBLAS, causing issues with some libraries and parts of Macaulay2. Try installing the community package [OpenBLAS-LAPACK](https://aur.archlinux.org/packages/openblas-lapack/) instead.
</details>

<details>
<summary>CMake is not using the local version of MPIR, Flint, etc.</summary>

Currently, when CMake is set to use the MPIR library, it compiles MPIR and a number of other libraries from source, including MPFR, NTL, Flint, Factory, Frobby, and Givaro. This is done to avoid linking conflicts caused by the libraries linking instead with the GMP library. Therefore, in order to link with system libraries the `-DUSING_MPIR=OFF` option is required. See this [comment](https://github.com/Macaulay2/M2/issues/1275#issuecomment-644217756) for more details on the reasoning behind this.
</details>

<details>
<summary><code>No download info given for 'build-flint' and its source directory</code></summary>

When building from a downloaded archive (i.e., not a git repository), it is necessary to also download and extract archives of the required submodules in the `M2/submodules` directory.

If a given library is not required on a particular system, CMake might still complain that the submodule directory is empty. One way to prevent this is to create a dummy file in the submodule directory for the libraries that are not required; for instance:
```
touch M2/submodules/flint2/empty
```
</details>

<details>
<summary>Detected library incompatibilities; rerun the build-libraries target</summary>

This message indicates that the build scripts detected an inconsistency between the libraries found on the system, and that those libraries are marked to be compiled from source. Run `ninja build-libraries` (or `make build-libraries`) to build the libraries from source.

If the problem persists, run `cmake --debug-trycompile` and open an issue with the contents of `CMakeFiles/CMakeError.log`.
</details>

<details>
<summary>macOS 10.15 Catalina issues with Clang and AppleClang</summary>

<b>Clang</b>: The Clang compiler installed via Homebrew or built from source typically includes OpenMP, but by default the system root is set to the Xcode SDK directory which does not contain the `libomp.dylib` library. The following command tells Clang how to find the correct library path:
```
export LIBRARY_PATH=`llvm-config --libdir`
cmake -S../.. -B. -GNinja -DCMAKE_BUILD_TYPE=Release
```
The `llvm-config` executable is typically located at `/usr/local/opt/llvm/bin/llvm-config`.

<b>AppleClang</b>: After ensuring that you have followed the usual steps from the [INSTALL](INSTALL) manual (e.g. running `xcode-select --install`, consider setting the `CMAKE_OSX_SYSROOT` variable to match the current SDK:
```
cmake -DCMAKE_OSX_SYSROOT=`xcrun --show-sdk-path` .
```
This would, for instance, tell CMake to look in `/Applications/Xcode.app/Contents/Developer/SDKs/MacOSX.sdk/usr/include` for headers.

Moreover, when building with MPIR, adding the following option allows CMake to find OpenMP from its own prefix rather than the common prefix at `/usr/local`, which may help avoid linking conflicts:
```
cmake -DCMAKE_SYSTEM_PREFIX_PATH=`brew --prefix libomp` .
```

If problems persist for either compiler, open an issue.
</details>

<details>
<summary><code>M2/include/M2/config.h:75:0: warning: "HAVE_ALARM" redefined</code></summary>

This error indicates that a previous in-source build has files left in the source tree. Run `make clean distclean` from the source directory or start from a clean clone of Macaulay2.
</details>

<details>
<summary><code>engine.h:84:3: error: ‘gmp_arrayZZ’ does not name a type; did you mean ‘gmp_newZZ’?</code></summary>

Same as above.
</details>

<details>
<summary><code>gmp-util.h:96:31: error: ‘gmp_CCmutable’ was not declared in this scope</code></summary>

Same as above.
</details>

<details>
<summary><code>mpirxx.h:3482:13: error: ‘mpir_ui’ has not been declared</code></summary>

This error indicates that a system version of `gmp.h` was found before `mpir.h`. If this occurs, open an issue.
</details>


<details>
<summary><code>undefined reference to `GC_malloc`</code></summary>

This error occurs if the GC library path is not set correctly.
<pre>
[  4%] Linking C executable scc1
CMakeFiles/scc1.dir/scc1.c.o: In function `getmem':
/home/macaulay/M2/M2/Macaulay2/c/scc1.c:23: undefined reference to `GC_malloc'
</pre>
Use the following command to tell CMake to build BDWGC:
```
cmake -DBUILD_LIBRARIES=BDWGC .
```
</details>


<details>
<summary><code>error: Runtime CPU support is only available with GCC 4.6 or later.</code></summary>

When compiling using Clang, the following error might occur if NTL was built with GCC instead:
<pre>
[ 25%] Building CXX object Macaulay2/e/CMakeFiles/M2-engine.dir/ntl-internal.cpp.o
In file included from M2/Macaulay2/e/ntl-debugio.cpp:4:
In file included from M2/Macaulay2/e/./ntl-interface.hpp:16:
In file included from /usr/include/NTL/ZZ.h:18:
In file included from /usr/include/NTL/lip.h:5:
/usr/include/NTL/ctools.h:510:2: fatal error: Runtime CPU support is only available with GCC 4.6 or later.
#error Runtime CPU support is only available with GCC 4.6 or later.
 ^
</pre>
Use the following command to tell CMake to build NTL:
```
cmake -DBUILD_LIBRARIES=NTL .
```
</details>


<details>
<summary>How to compile with Intel(R) Math Kernel Library</summary>

[MKL](https://software.intel.com/en-us/mkl) is a linear algebra routines library specifically optimized for Intel(R) processors. To enable linking with MKL, adjust the path and architecture appropriately and run the following before calling `cmake`:
<pre>
source /opt/intel/bin/compilervars.sh intel64
</pre>
Note that MKL is closed-source but released as a freeware.

See [FindLAPACK](https://cmake.org/cmake/help/latest/module/FindLAPACK.html) for information on specifying the linear algebra library by setting the value of `BLA_VENDOR` in `cmake/check-libraries.cmake`.
</details>


<details>
<summary>How to compile with AMD(R) Optimizing CPU Libraries</summary>

TODO: [AOCL](https://developer.amd.com/amd-aocl/) includes AMD BLIS and AMD libFLAME
</details>