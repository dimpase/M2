# RingElement/Ring refactor proposal #

Work in progress, current document written by Jay Yang building on a discussion with Michael Stillman. Comments and contributions welcome

Broadly speaking I have the following goals in this proposal in approximate order of priority:

- Make the code more exception safe
- No performance losses, possibly small gains
- Document the actual Ring/RingElement/ARing interface
- Make the code easier to use correctly (fewer memory leaks)
- Make the code more like C++ code and less like C code
- Faster (or at least not slower) compile times

## C++ interface structure ##

### Public Interface ###

Note we don't directly inherit from EngineObject
RingElement is pure virtual, we can have implementations inherit from
either EngineObject or if needed MutableEngineObject.

```c++
class RingElement{
public:
    //pure virtual functions
    virtual bool is_unit() const = 0;
    //I'm torn whether operator notation is actually helpful for us
    //the type returned is "wrong" such that we can't write a*b*c
    virtual RingElement* operator*(const RingElement& other) const = 0;
    //i.e. does the following read better or worse a->mult(b)
    virtual RingElement* mult(const RingELement* other) const = 0;
    ...
};
```

```c++
class Ring{
public:
    virtual ~Ring() = 0;
    //pure virtual funtions
    virtual RingElement from_int(int i) const = 0;
    ...
};
```

The instances of ring might need to be public.
On the otherhand, we might be able to get away with factory functions.
So either we have classes like this as part of the public interface

```c++
template<class R>
class ConcreteRing<R> : Ring{
    ...
};
```

Or we make functions like this part of the public interface

```c++
Ring *makeZZp(int p);
Ring *makePolynomialRing(...);
```


### Internal Interface ###

We will also have an internal interface that engine code that manipulates RingElement and Ring use.

We have a templated type RingElementImpl that implements the actual code for RingElement.
But we don't expect/need an default implementation.

```c++
template<class R>
class RingElementImpl<R> : RingElement{
//no default implementation
}
```

Instead we have specializations for each ring that detail the actual structure. It should be approximately
as follows

```c++
template<class RT>
class RingElementImpl<ConcreteRing<RT> > : RingElement{
private:
    const ConcreteRing<R> &ring;
    R::ElementType val;
public:
    //actual implementations of the functions in RingElement
};
```

A RingInterface or ARing class should implement at least the following types and functions.

```c++
class RingInterface{
public:
    //This is a intended to be a zero cost wrapper around the C type.
    //Importantly, by having an initializer, it follows
    //RAII principles and is more exception safe.
    //Note that in general a default constructor is not possible, so for arrays
    //placement new will be needed.
    struct ElementType{
    public:
        using ValueType = ...;
        //this allows using ElementType transparently for C code that expects ValueType
        operator const ValueType&() const;
        operator ValueType&();
        ElementType(const RingInterface& ri);//initialize as appropriate
        //Be careful about adding copy constructors, it's not usually useful
        ElementType(ElementType&& v);//allow moves (otherwise returning from functions is hard)
        ~ElementType();//this should infact cleanup the type
    private:
        ValueType value;
    }
    //Modern compilers should always be able to optimized the copy/move in the
    //return away. but I'm not 100% certain how reliable it is
    //the alternative signature is void add(ElementType& out, const ElementType& a, const ElementType& b) const;
    ElementType add(const ElementType & a, const ElementType& b) const;
    //all the other arithmetic operations

    //TODO think about conversion/initialization functions
}
```

Unless there's a good reason to, RingInterface instances should NOT be garbage collected, preferably, they will be direct members of the appropriate ConcreteRing class.

The justification for having `RingInterface` and `Ring` separate is so that code that does not need to use the frontend `RingElement` can directly manipulate `RingInterface::ElementType` instances.

Note that `RI::ElementType` replaces `ARingElement<RI>` for most operations, but if the element needs to remember what ring it belongs to `RingElementImpl<RI>` should be used instead.


## C interface structure ##

Its not clear to me how much we actually need a C interface, but for that we have something like this. The templates are mostly not exposed, so the C interface is mostly straightforward

```c
class Ring;
class RingElement;

//function prototype examples
Ring *makeRing(...);
RingElement *makeRingElement(Ring* r,...);
RingElement *add(const RingElement *a, const RingElement *b);
Ring *makePolynomialRing(Ring *coeff,...);
```

## Implementation Parts ##

This is a proposed implementation strategy.

### Part 1: Refactor RingInterface ###

The goal here is to refactor all RingInterfaces instances to follow the template outlined above. This will involve changing most of the uses of ElementType. This should be performance neutral if done correctly, and will solve most of the exception safety issues related to RingElements. And while invasive from a lines of code perspective, it doesn't fundamentally change how any of the code works

### Part 2: Interface ###

Add a shim layer on top of the current code implementing the desired c++ interface.
This will obviously be bad for performance, but this will test if the interface proposed is usable


### Part 3: Remove ring_elem ###

The goal here is to remove the somewhat messy `ring_elem` union. This will involve actually implementing `RingElementImpl<R>` for all the rings. This change should get most of the performance lost in step 2 back

### Step 4: Cleanup ###

As a consequence of the previous steps, functions and implementations might end up in inconsistent places. The goal here is to have a consistent idea of where a function should go and follow that.


## Known Caveats ##

This new code is more template heavy overall, and so more care needs to be taken to ensure that the templates don't cause long compilation times.

It's annoying not to be able to default construct `RingInterface::ElementType` objects, but this is needed for correctness in the general case. In particular this means that arrays of `RingInterface::ElementType` either needs special support functions or placement new.

It's not clear that everything can be written as a `ConcreteRing<R>`  without resorting to specialization. Polynomial rings in particular are non-obvious.

## Other Possible Goals ##

Is it possible to move the ring element stuff into a separate namespace/directory? i.e. separate the concern of translating between M2 and C++ with the concern of actually doing math.

## Notes ##

Currently integers and other "numbers" work differently than RingElements,
A question is whether they should be made to be RingElements.

Current multiplication process

if we have two `RawRingElement` a,b at the d level, assume then are of some `ConcreteRing<RT>` instance

- `a*b` 
- `RingElement::operator*` (in relem.cpp)
- `Ring::mult` (virtual)
- `ConcreteRing<RT>::mult` (in aring-glue.hpp)
- `RT::mult` (in aring-*.hpp depending on RT)

"New" multiplication process

- `a*b`
- `RingElement::operator*` (virtual)
- `RingElementImpl<ConcreteRing<RT>>::operator*`
- `RT::mult`

In practice, this seems to be about the same number of indirections.

Because there isn't this ring_elem intermediary, we can probably give RingElement a finalizer, but there is a serious question about cost. In particular, how expensive are finializers really?

Finalizers are really expensive, but the disclaim system is much faster.
