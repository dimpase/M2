## What are hooks?
Hooks are a way for functions and methods to use different algorithms for different purposes. For example, the algorithm run by `minimalPresentation M` will be different if `M` is a homogeneous module over an affine ring, or if `M` is a module over the ring of integers. If the user wants to implement a new algorithm for computing minimal presentations for a specific type of module, they can add it as a hook, which could be run using the existing function `minimalPresentation M`. 

## A minimal example
We will create a function `foo` that takes an integer as input, and print different messages based on the input. To use hooks, the function has to run `runHooks`
```macaulay2
foo = method(Options => {})
foo ZZ := opts -> i -> runHooks(ZZ, symbol foo, (opts, i))
```
We will create a couple of hooks. **Note that currently each hook has to return the value using `break`.**
```macaulay2
f = (opts, i) -> (
  if i == 0 then(
    <<"In f"<<endl;
    break 24
  )
)

g = (opts, i) -> (
  if i == 10 then(
    <<"In g"<<endl;
    break 13
  )
)
```
The hooks can be added using `addHook`.
```macaulay2
addHook(ZZ,symbol foo, f)
addHook(ZZ,symbol foo, g)
```
Now `foo 0` returns 24, and `foo 10` returns 13. For any other input `foo` returns `null`.

Hooks are run in order from the most recent to the oldest. To demonstrate this, we add a hook that will override `f`
```macaulay2
addHook(ZZ, symbol foo, (opts,i) -> if i <= 0 then break 999)
```
`foo 0` will now return 999.

## Notes
* Only functions that call `runHooks` can use hooks.
* If your function uses hooks, this should be mentioned in the documentation
* Hooks are run in order until one of them hits `break`. Because of this, hooks should be able to check quickly whether or not they should be run