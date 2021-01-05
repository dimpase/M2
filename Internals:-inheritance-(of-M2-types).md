### Creating new subtypes
The method `new Type of Foo` creates a new type that inherits from `Foo`. Consider the snippet below

```macaulay2
X0 = new Type of BasicList
X1 = new Type of X0
```

Any method that accepts a `BasicList` will also accept an instance of `X0` and `X1`, and any method that will accept an instance of `X0` will also accept an instance of `X1`. The list of ancestors of a type can be viewed with `ancestors`.