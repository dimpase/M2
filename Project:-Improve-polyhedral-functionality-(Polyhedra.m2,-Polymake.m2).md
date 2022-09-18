For polyhedral computations in M2 one can use Polyhedra.m2, and, for extended functionality, Polymake.m2 to interact with [polymake](https://polymake.org/doku.php). This project page will for now just contain notes on possible improvements.

# Improve convex hull computations
Currently computation of convex hulls, i.e. getting the vertices from a description via halfspace inequalities, is done via `FourierMotzkin.m2`. There is already code for interfacing `lrs` and `cdd`, but this is not accessible in a nice way.
- What would be a nice way to let the user chose between those three alternatives? There is no unique best choice here, depending on the concrete example one or the other may be faster. In some cases only one of the three terminates.
- M2 comes with both lrs and cdd (or at least one of these). Figure out the technical details on how to access these. The toplevel implementation currently uses a system-wide installation of lrs/cdd.

# Update Polymake.m2
Polymake.m2 interfaces polymake via writing and reading files. It writes a polyhedral object, then runs polymake on this file, and finally reads the output.
- Figure out whether Polymake.m2 still uses XML. Switch to JSON.
- Independently of whether polymake is installed, it makes sense for Polyhedra.m2 to rely on Polymake.m2 for storing its objects as JSON.
- Update Polymake.m2 to most recent polymake version.
- Add some kind of switch for the user in Polyhedra.m2 to use polymake as a backend, if it is installed. What should the default be?
- ~~Should there be a separate JSON package? (Is there already?) This could be useful for many other data types as well.~~  _Finished -- see [#2589](https://github.com/Macaulay2/M2/pull/2589)_

# C++ interface to polymake
polymake can also be interfaced on the C++ level, via libpolymake. The api of libpolymake has stabilized and big changes are not to be expected for the near future. Hence it makes sense to also interface polymake on the engine level, especially since this will be faster than writing and reading files, and also more stable.
- Figure out how to convert M2 matrices and vectors to polymake and back. Once this is done, a lot of functionality becomes available, nevertheless this approach is less flexible than via Polymake.m2.
- Introduce a precompiler flag for building with polymake, not everyone will have it installed.
- Think about distribution. Maybe it is enough to have the Ubuntu version come with polymake, since libpolymake comes via the package manager there.

# Smaller tasks
- Figure out whether polyhedral complexes can be intersected. If not, implement it.