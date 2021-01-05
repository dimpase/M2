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
X1 ** Y0 := (x, y) -> "X1 ** Y0"
```
Note that `(new X1) ** (new Y0)` and `(new X1) ** (new Y1)` will both work, since `Y1` inherits from `Y0`. Furthermore, `(new X0) ** (new Y1)` will not work, as `X0` is an ancestor of `X1`. The function that gets called with given types can be recovered using `lookup`, e.g. `lookup(symbol **, X1, Y1)` will return the function above that returns the string `"X1 ** Y0"`.

### Hashcodes

For garbage collection purposes, the method is installed in the youngest type with respect to the hashcode via the function `hash`. The function `youngest` returns the youngest of two things. In this case, the method is stored under `Y0`, see e.g. `peek Y0`. Note that the hashcode reflects the age of mutable objects only.

### .d code

