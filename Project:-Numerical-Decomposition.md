* **Current people involved**: [Tim Duff](https://timduff35.github.io/timduff35/), [Anton Leykin](https://antonleykin.math.gatech.edu/), [Jose Rodriguez](https://people.math.wisc.edu/~jose/) 
* **Goal**: implement numerical irreducible decomposition for multiprojective varieties and related tools
* **Current status**: under development

## Project Description

Give a variety embedded in a product of projective spaces that is given by a system of multihomogeneous polynomial equations, we would like to describe it using (collections) of _witness sets_. (A _witness set_ is a cornerstone concept of _numerical algebraic geometry_.)

The current plan is to 
* implement most of the tools described in [1], 
* revamp the current implementation (in `NumericalAlgebraicGeometry` package) of decomposition in the case of ambient affine/projective space (a single factor case) using _u_-generation in [2], 
* work on multiprojective _u_-generation in [2].
 
### Examples
The old implementation of the numerical decomposition of an affine variety:
```
i1 : needsPackage "NumericalAlgebraicGeometry";
...
...
...
i5 : R = CC[x,y,z];
i6 : sph = x^2+y^2+z^2-1;
i7 : I = ideal {x*sph*(y-x^2), sph*(z-x^3)};  
o7 : Ideal of R
i8 : numericalIrreducibleDecomposition I   
o8 = a numerical variety with components in      
     dim 1:  (dim=1,deg=1) (dim=1,deg=3)      
     dim 2:  (dim=2,deg=2)  
o8 : NumericalVariety
```

### References (that describe the math and/or algorithms)

[\[1\]](https://arxiv.org/abs/1908.00899) A numerical toolkit for multiprojective varieties  

Authors: [Jonathan D. Hauenstein](https://arxiv.org/search/?searchtype=author&query=Hauenstein%2C+J+D), [Anton Leykin](https://arxiv.org/search/?searchtype=author&query=Leykin%2C+A), [Jose Israel Rodriguez](https://arxiv.org/search/?searchtype=author&query=Rodriguez%2C+J+I), [Frank Sottile](https://arxiv.org/search/?searchtype=author&query=Sottile%2C+F)

[\[2\]](https://arxiv.org/abs/2206.02869) _u_-generation: solving systems of polynomials equation-by-equation

Authors: [Timothy Duff](https://arxiv.org/search/?searchtype=author&query=Duff%2C+T), [Anton Leykin](https://arxiv.org/search/?searchtype=author&query=Leykin%2C+A), [Jose Israel Rodriguez](https://arxiv.org/search/?searchtype=author&query=Rodriguez%2C+J+I)