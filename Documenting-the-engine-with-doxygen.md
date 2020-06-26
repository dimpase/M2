Building the engine documentation is [Step 1 here.](https://github.com/DanGrayson/Internals/blob/master/25-6-2020/engine-doc-hw)

Documenting an entity such as a class can be done in a [variety of ways](https://www.doxygen.nl/manual/docblocks.html#docstructure). For example, we have the excerpt.

``
/** 
@ingroup gb
    @brief base class for Groebner basis computations.
*/

class GBComputation : public Computation
``
 
The @brief description can then be read on the documentation page of the documentation page for GBComputation in the browser. 

The documentation pages [grouped](https://www.doxygen.nl/manual/grouping.html) together in various ways. This includes a full list of classes and namespaces. Individual documentation pages contain inheritance and call diagrams, as well as the underlying source.

For the purpose of grouping, is also the possibility of creating Modules which can be documented together. The @ingroup command above puts GBComputation in the GroebnerBasis (aka gb) module.

[Here](https://www.doxygen.nl/manual/commands.html) is full list of commands.