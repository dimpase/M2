### Creating new subtypes
The method `new Type of Foo` creates a new type that inherits from `Foo`. Consider the snippet below

```macaulay2
X0 = new Type of BasicList
X1 = new Type of X0
```

Any method that accepts a `BasicList` will also accept an instance of `X0` and `X1`, and any method that will accept an instance of `X0` will also accept an instance of `X1`. The list of ancestors of a type can be viewed with `ancestors`.

### Looking up methods
Let's create two new types, and install a method that prints a message
```macaulay2
Y0 = new Type of BasicList
Y1 = new Type of Y0
X0 ** Y1 := (x, y) -> "X0 ** Y1"
```
Note that `(new X0) ** (new Y1)` and `(new X1) ** (new Y1)` will both work, since `X1` inherits from `X0`. Furthermore, `(new X0) ** (new Y0)` will not work, as `Y0` is an ancestor of `Y1`. The function that gets called with given types can be recovered using `lookup`, e.g. `lookup(symbol **, X1, Y1)` will return the function above that returns the string `"X0 ** Y1"`.

### Hashcodes

For garbage collection purposes, the method is installed in the youngest type with respect to the hashcode via the function `hash`. The function `youngest` returns the youngest of two things. In this case, the method is stored under `Y1`, see e.g. `peek Y1`. Note that the hashcode reflects the age of mutable objects only.

### .d code
In the d language, the file `hashtable.dd` installs the lookup functions, which decide which methods get called with inherited types. The function `lookupfun(...)` implements the top-level `lookup` function, and uses `lookupBinaryMethod`, `lookupTernaryMethod`, etc... The lookup works by looking at the rightmost type first, and looping through all ancestors. If no method is found, the next argument is replaced by its parent and the rightmost type loops through all arguments. For example, the method `(new X1) ** (new Y1)` calls the method defined above by trying to find
```macaulay2
(symbol **, X1, Y1)
(symbol **, X1, Y0)
(symbol **, X1, BasicList)
(symbol **, X1, Thing)
(symbol **, X0, Y1) -- found!
``` 
