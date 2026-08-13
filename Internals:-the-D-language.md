*This page was written by Claude (Anthropic's Claude Code), working from the
compiler source in `M2/Macaulay2/c`; every "Try it" below was run against a
built `scc1` before being written down.*

**D** is the language the Macaulay2 interpreter is written in. Its sources are
in `M2/Macaulay2/d`; its compiler, `scc1`, is in `M2/Macaulay2/c` and translates
one `.d` file to C, or one `.dd` file to C++.

This page began as notes taken by Gwyn Whieldon at an early Macaulay2 internals
workshop, recording Dan Grayson's lecture on the D language. The lecture's
files — a `Makefile`, a 29-line `foo.d`, and a page of exercises — are still in
Grayson's [Internals](https://github.com/DanGrayson/Internals) repository, and
`foo.d` is the running example throughout this page. The reference material
around it was added later and is derived from the compiler source, with file
and line citations so you can check any claim.

For syntax proper — tokens, operator precedence, EBNF — see
[D language grammar](D-language-grammar). Its companions are the
[Macaulay2 language grammar](Macaulay2-language-grammar) and the
[SimpleDoc language grammar](SimpleDoc-language-grammar).

## Contents

1. [Setup, and the file we compile](#setup-and-the-file-we-compile)
2. [Compilation model](#1-compilation-model)
3. [Types](#2-types)
4. [Declarations](#3-declarations)
5. [Statements and control flow](#4-statements-and-control-flow)
6. [Memory and GC](#5-memory-and-gc)
7. [Static checks](#6-static-checks)
8. [Name mangling](#7-name-mangling)
9. [Idioms worth knowing](#8-idioms-worth-knowing)
10. [Traps](#9-traps)
11. [Working on the code](#working-on-the-code)

---

## Setup, and the file we compile

You need a successfully built Macaulay2. Find `Macaulay2/c/scc1` in your build
directory and put it on your `PATH`.

Then create a directory containing this `Makefile`, which is Grayson's
[from the lecture](https://github.com/DanGrayson/Internals/blob/master/dan/D%20language/Makefile):

```make
all : foo
foo : foo.d
	scc1 -noline -debug foo.d
	mv foo-exports.h.tmp foo-exports.h
	scc1 -typecodes
clean : ; rm -f *.tmp *-tmp.c typecode.db *-exports.h *.log *.out *.sym
```

and this `foo.d`, which is Grayson's
[example file](https://github.com/DanGrayson/Internals/blob/master/dan/D%20language/foo.d):

```d
b := true;
export c := 345;
(x:int) + (y:int) ::= Ccode(int,"(",x," + ",y,")");
d := 2 + 2;
i := if b then 11 else 22;
X := {  x:int, y:int};
Y := {+ a:int, b:int, c:bool};
Z := {+ d:int, e:int};
z := Z(3,4);
W := tarray(Z);
WW := tarray(Z);
WWW := tarray(Z);
WWWW := tarray(Z);
U := Y or Z or tarray(Z);
foo ( u:U ) : int := (
     when u
     is y:Y do y.a
     is z:Z do z.d
     is w:WWW do 44
     );
w := new WWW len 2 do provide z;
u := U(w);
bar () : U := Y(111,222,true);
car () : U := Z(333,444);
u1 := bar();
u2 := car();
foo(x:int,y:int):int := 2;
export foo():int := 1;
export foo(x:int):int := 1;
```

Twenty-nine lines, and between them they exercise most of this page: the three
kinds of definition, a macro-defined operator, `if` as an expression, tagged and
untagged structs, arrays, a union, `when`, `new … provide`, and three
overloads of one name. You cannot *run* the result — there is no `main` — but
you can read the C, which is the point.

**One thing to know before you start.** `make` fails:

```
foo.d:19:10: error: type not among those represented by the when-clause
foo.d:16:5: error: missing case 3
foo.d:22:0: error: symbol being redefined
foo.d:15:6: error: here is the previous definition
```

The union is declared as `Y or Z or tarray(Z)`, and the `when` tries to match
`WWW`. Both `WWW` and that anonymous `tarray(Z)` are *tagged* array types, and
tagged types are never identified with one another however alike they look
(see [Type identification](#type-identification)) — so the union's third member
is a type with no name, `WWW` is not among the union's members, and the third
case of the union goes uncovered. The two later errors are a cascade off the
first. Change line 14 to name the type:

```d
U := Y or Z or WWW;
```

and the file compiles clean. Everything below refers to the fixed file.

**A warning about the examples on this page.** Most are quoted from the
interpreter, where every file begins `use arithmetic;`. A file that does not
has no arithmetic at all: not `+`, not `<`, and not even a negative literal —
`q := -1;` fails with *"not a function or type"*, because unary minus is a
macro too. That is why `foo.d` opens by defining `+` for itself. To experiment
in a standalone file, define the operators you need the same way, or add a
`use arithmetic;` and an `-I` pointing at the `.sig` files in a built tree.

---

## 1. Compilation model

### The pipeline

`scc1` compiles one file at a time. Given `foo.d` it writes
(`scc1.c:279–370`):

| Output | Content |
| --- | --- |
| `foo-tmp.c` | the translated code, opening with `#include "foo-exports.h"`, then `scc-core.h` and `supervisorinterface.h` (`scc1.c:158–161`), then every `header "…"` string |
| `foo-exports.h.tmp` | an include guard, every `declarations "…"` string, fixed boilerplate (`scc1.c:124–148`), then the generated typedefs |
| `foo.sig.tmp` | the package's signature — regenerated **D** source, not C |
| `foo.dep.tmp` | makefile dependencies on the `.sig` files reached through `use` |
| `foo.out`, `foo.log`, `foo.sym` | only with `-debug`: parse tree, lowered tree, symbol/type/string tables |

> **Try it.** Run `make`. Besides the database `typecode.db`, you get seven
> files. `foo-tmp.c` is the code,
> `foo-exports.h` the declarations — note that the *types* declared in `foo.d`
> appear only in the header, which is what the third `make` line is for. The
> signature is short, and describes only what other files could `use`:
>
> ```
> -- generated by scc1
>
> signature foo (
>      import c:int;
>      import foo():int;
>      import foo(x:int):int;
> );
> ```
>
> Three exports, and each `export` in the source has become an `import` in the
> signature (`cprint.c:936`), which is exactly what a consumer needs.
> `foo.dep.tmp` is empty because `foo.d` has no `use` line.
>
> The last `make` line runs `scc1 -typecodes`:
>
> ```
> #define Y_typecode 2
> #define WWW_typecode 3
> #define Z_typecode 1
> ```
>
> Three of the eight types declared got a code. These numbers live in a GDBM
> database, `typecode.db`, sitting next to the source, and they persist across
> compilations — delete it and recompile and the numbering starts over. See
> [Type codes](#type-codes).

A `.dd` file writes `foo-tmp.cc` instead, compiled by the C++ compiler. That is
the *entire* difference: `do_this_cxx` is consulted in exactly one place, the
output file name (`scc1.c:276, 290`). The lexer and grammar never see the
extension, so **D itself is identical in `.d` and `.dd`**. `-cxx` forces `.cc`
output for a `.d` file.

`.dd`-ness is contagious, and the reason is worth understanding —
`chrono.dd:16–19` says it directly:

```
-- The typedef from this type declaration is put into the include file chrono-exports.h,
-- so that means we can write "use chrono;" only in a *.dd file, not in a *.d file.
-- That's why we are renaming interp.d to interp.dd.  Eventually all *.d files should
-- be renamed.
```

If a package's `declarations` mention a C++ type, its `-exports.h` is C++, so
every package that `use`s it must be `.dd` too.

Build-system side: suffix rules at `M2/include/config.Makefile.in:158–186`;
CMake does the same mapping (`d`→`c`, `dd`→`cc`) in `M2/cmake/scc.cmake:17–46`.

### Packages

Every file is implicitly wrapped in `package <file stem> ( … )`
(`grammar.y:50–58`), the stem being the basename with directory and extension
stripped. **The package name is the filename**, so a `.d` file must not be named
after a type the compiler already knows about.

A file also may not define a symbol with its own name: `neg.d` containing
`neg := 1;` fails with *"symbol being redefined"*, reporting a previous
definition on a line the file does not have. The package symbol got there first.

Per package, `chkpackage1` (`chk.c:1169–1240`) synthesises three C functions.
Their names carry a *double* underscore, because the package prefix ends in one
and the suffix begins with one:

- `<pkg>__prepare` — the initializer. Emitted with `__attribute__((constructor))`
  (`cprint.c:487`) so the linker runs it before `main`, and guarded by a
  `static int called_yet` so it runs once (`chk.c:1207–1209`).
- `<pkg>__thread_prepare` — pushed onto a runtime `thread_prepare_list`
- `<pkg>__final` — pushed onto `final_list`

`use foo;` emits a call to `foo__prepare()` (`chk.c:2626`).

> **Try it.** Everything at file scope in `foo.d` — `b := true`, `d := 2 + 2`,
> the `new` array, the calls to `bar()` and `car()` — ends up inside one
> generated function:
>
> ```c
> void foo__prepare(){
>   int tmp_; Z tmp__1; …           /* a temporary per expression that needs one */
>   static struct FUNCTION_CELL this_final, this_thread_prepare;
>   static int called_yet = 0;
>   if (called_yet) return; else called_yet = 1;
>   b = 1;
>   foo_c = 345;
>   d = (2 + 2);
>   …
> ```
>
> and `foo-exports.h` declares it as
> `extern void foo__prepare() __attribute__ ((constructor));`.

Explicit `package name ( … )` syntax exists but is unused.

Because top-level expressions run at load time in file order, link order
matters. `classes.dd` is 82 consecutive `setupconst(…)` calls at file scope, and
`interp.dd` is listed last in both `d/Makefile.files.in:110` and
`d/CMakeLists.txt:97`, with the comment "this one is last, because it contains
the top level interpreter".

### `use`, and the `.sig` mechanism

`chk_use` (`chk.c:2582–2636`):

1. If the package is unknown, find `<name>.sig` along `sigpath` (initially `.`,
   extended by `-I`), parse it, and check it. Failure →
   *"undefined package (no *.sig file found)"*.
2. Record a make dependency in `foo.dep.tmp`.
3. Detect `package_active_F` → *"circular package dependency"*.
4. Emit the `<pkg>__prepare()` call, unless we are inside a signature.
5. Re-intern every symbol from the package's export list into the current scope,
   and re-export them from the enclosing package — so `use` is **transitive**.
6. Reproduce the `use` line in this package's own `.sig`.

A `.sig` file is generated D source using the `signature` form. A real one, from
the build tree (`Macaulay2/d/chrono.sig`):

```
signature chrono (
     use arithmetic;
     ...
     declarations "#include <chrono>";
     import cpuTimer(c:Code):Sequence;
     import wallTimer(c:Code):Sequence;
);
```

The package dependency graph must be acyclic. Mutual recursion across files
therefore goes through a mutable variable holding a function; see
[Idioms](#8-idioms-worth-knowing).

Operational consequence, from `Macaulay2/c/README:94–98`: *"always run make
twice before giving up on mysterious errors, as the first time, the translator
may correct an erroneous `*.dep` file or `*.sig` file."*

### Command-line options

Complete set, `scc1.c:168–186` and `195–273`:

| Option | Effect |
| --- | --- |
| `--help`, `-v` | usage, version |
| `-cxx` | emit `-tmp.cc` rather than `-tmp.c` |
| `-dep` | stop after `.dep.tmp` and `.sig.tmp` |
| `-noline` | suppress `# line` directives (`cprint.c:149–154`). Used for exactly one file: `pthread-tmp.c` in `d/Makefile.in` |
| `-noarraychks` | omit array bounds checks |
| `-nocasechks` | omit `when` type-tag and null checks |
| `-O` | both of the above |
| `-nomacros` | skip the built-in operator prelude — this removes `:=`, `.`, `+`, … from the language |
| `-pthreadlocal` | use `TS_Get_Local` rather than `__thread`; already the default (`scc1.c:17`) |
| `-typecodes` | dump `typecode.db` as `#define`s and exit |
| `-tabwidth N` | column arithmetic for diagnostics (default 8) |
| `-yydebug` | bison trace |
| `-debug` | write `.out`, `.log`, `.sym`; enables extra `GC_CHECK_CLOBBER` instrumentation |
| `-Ixxx` | append to the `.sig` search path |

`-sig` is listed in the usage text but is not parsed in `main`. Note that `--`
is not an option prefix; it is the comment marker.

---

## 2. Types

### Built-in types

Created by `basictype()` from `init_dictionary()` (`dictionary.c:54–107`).

| D name | Emitted C | Notes |
| --- | --- | --- |
| `int` | `int` | array indices, array lengths, integer constants, `for`/`new` loop indices |
| `char` | `signed char` | spelled explicitly "for uniformity across compilers" (`dictionary.c:77–78`) |
| `bool` | `char` | `dictionary.c:81–82`; `true`→`1`, `false`→`0` |
| `double` | `double` | |
| `void` | `void` | a function returning nothing; also the type of `(a;b;)` |
| `null` | `void *` | the type of the null pointer; the value is `null()` |
| `exits` | `void` | an expression control never returns from — `Ccode(exits,"exit(0)")` |
| `returns` | `returns` | an expression that never falls off its end but may return — `Ccode(returns,"return 1")` |
| `package` | — | the type of a package symbol |
| `Type` | — | the type of types; `type(e) == type__T` is how the checker knows `e` is a type expression |

`returns` is **unchecked** — nothing verifies that the C string actually returns,
or returns a value, so `README:158–160` advises compiling with
`-Wreturn-type -Werror`.

Two internal types round it out: `deferred_` (a symbol whose type isn't known
yet) and `bad_or_undefined_` (an error sentinel that `subtype()` accepts against
anything, `type.c:844`, to stop error cascades).

`ushort`, `ulong`, `short`, `long`, `uint`, `uchar`, `float`, `size_t`,
`hash_t` and the `intN_t` family are *not* built in. They are ordinary D
declarations in `arithmetic.d:11–29`:

```d
export size_t := integerType "size_t";
export ushort := integerType "unsigned short";
export float  := arithmeticType "float";
```

as is `nothing`: `export nothing := void();` (`arithmetic.d:10`).

### Type constructors

| Form | Meaning |
| --- | --- |
| `array(t)` | pointer to variable-length array of `t` — carries an `int len` field |
| `array(t,n)` | fixed length `n`; **no** `len` field, so it cannot be used as a variable-length array (`README:194–195`) |
| `tarray(t)`, `tarray(t,n)` | the same, plus a leading `unsigned short type_` tag |
| `{a:t, b:u}` | pointer to struct |
| `{+a:t, b:u}` | pointer to *tagged* struct — first field is a small integer naming the type |
| `t or u or …` | union; see below |
| `function(t,u):w` | function pointer |

Checked by `chkarray` / `chktarray` / `chkobject` / `chkor` / `chkfunction`
(`chk.c:1880–2108`). Layout is emitted by `cprintarraydef` (`cprint.c:285–301`).
A struct member of type `void` is skipped in the layout (`cprint.c:313`) but
still occupies an argument slot in a constructor call; an all-`void` struct gets
a `char _;` filler. Two pseudo-members always resolve on any array: `len` and
`type`, both `int` (`type.c:133–135`).

Fixed-length arrays and empty tagged structs both work: `MutexArray :=
array(ThreadMutex,49);` (`hashtables.dd:57`), `export nullCode := {+};`
(`parse.d:227`).

> **Try it.** `X`, `Y` and `Z` in `foo.d` differ by one character. Look at
> `foo-exports.h`:
>
> ```c
> struct X_struct BASECLASS {int x;int y;};
> struct Y_struct BASECLASS {unsigned short type_;int a;int b;char c;};
> struct Z_struct BASECLASS {unsigned short type_;int d;int e;};
> ```
>
> The `+` is what prepends `type_`. Note also `char c` for the `bool` member,
> and that the four array types
>
> ```c
> struct W_struct {unsigned short type_;int len;Z array[];};
> struct WW_struct {unsigned short type_;int len;Z array[];};
> ```
>
> carry both the tag and the `len` field. Now delete the `+` from `Y` and
> recompile:
>
> ```
> untagY.d:14:5: error: untagged type not usable with other non-null types in a union type
> untagY.d:7:0: error: ... here is the declaration
> ```
>
> A union of several members has to read a tag at run time, so every member
> needs one. Six more errors follow those two — the union symbol never gets
> defined, so the `when` reports that it has no union type, `U` is "never
> declared", and so on. **Fix the first error and recompile**; most of a D
> error list is usually cascade.

### Union types

`chkor` (`chk.c:2078–2108`) enforces three rules:

1. Every member is a pointer type or `null`, else *"expected a pointer type"*.
2. If more than one member is not `null`, **every** non-`null` member must be
   tagged, else *"untagged type not usable with other non-null types in a union
   type"* — because dispatch has to read a tag at run time.
3. Members not yet defined are recorded as needing to be pointers/tagged, and
   re-checked when the definition arrives (`type.c:88–106`).

Representation (`cprint.c:339–351`):

- With ≥2 non-`null` members the union is *composite* and becomes
  `struct tagged_union *`, i.e. `{ unsigned short type_; }`.
- With exactly one non-`null` member it is **free** — it compiles to that
  member's own C type, with `null` represented by a null pointer.

That distinction drives codegen for `when`, and explains a comment at
`chk.c:761`: *"we don't examine the type tag when there is only one non-null type
in the union, because it might not be there."*

> **Try it.** Compile
>
> ```d
> Z := {+ d:int, e:int};
> Y := {+ a:int};
> Free := Z or null;
> Comp := Z or Y;
> ```
>
> and read the typedefs:
>
> ```c
> typedef Z Free;
> typedef struct tagged_union * Comp;
> ```
>
> A free union *is* its member at the C level. `foo.d`'s `U` has three non-null
> members, so it is composite, and `u := U(w)` compiles to a plain cast,
> `u_1 = ((U)w_1);`.

`interntype` also computes `commons` (`type.c:364–387`) — the leading fields
shared by every non-`null` member — which is what lets you write `x.field`
directly on a union value.

**Subtyping exists only for unions** (`subtype()`, `type.c:837–868`): `s ≤ t`
when every member of `s` has a supertype in `t`, and a single type is `≤` a union
containing it. For everything else the compiler assumes structural
identification has already made equivalent types identical — which is the next
section.

### Foreign types

Six constructors, each taking a C type name as a string literal. All six lex as
the single token `STRINGOP`.

| Form | Flag | Meaning |
| --- | --- | --- |
| `Pointer "T"` | `raw_pointer_type_F` | pointer to memory that may contain GC pointers |
| `atomicPointer "T"` | `raw_atomic_pointer_type_F` | pointer to pointer-free memory |
| `Type "T"` | `raw_type_F` | opaque value type that may contain GC pointers |
| `atomicType "T"` | `raw_atomic_type_F` | opaque value type that contains none |
| `arithmeticType "T"` | `arithmetic_type_F` | castable to/from other arithmetic types |
| `integerType "T"` | `integer_type_F \| arithmetic_type_F` | ditto, integral |

Examples: `export charstar := atomicPointer "char *";` (`M2.d:14`);
`export atomicField := Type "struct atomic_field";` (`atomic.d:15`);
`Chrono := Type "std::chrono::steady_clock::time_point";` (`chrono.dd:20`);
`export Thread := arithmeticType "pthread_t";` (`pthread0.d:11`).

Note that `atomic` is not a keyword — `atomic.d` is an ordinary D package
wrapping C11 atomics in `Ccode` macros. Nor is `Boolean` built in:
`export Boolean := {+v:bool};` (`parse.d:344`).

### Construction and casting

`chknewinstance` (`chk.c:1728–1878`) handles `T(…)` whenever the head has type
`Type`:

- **basic type** — `null()` is a cast of 0; `void()` is nothing; otherwise one
  argument, arithmetic to arithmetic, else *"impossible type conversion"*.
- **array/tarray** — allocate, set `len`, assign elements; fixed length must
  match (*"wrong number of initial values"*).
- **union** — exactly one argument, which must be a subtype
  (*"type conversion requires one argument"*, *"type of argument not among those
  in the union"*).
- **struct** — one argument per non-`void` member (*"too many arguments"* /
  *"too few arguments"*). `self` inside the argument list refers to the object
  being built, which is how cyclic structures are made:
  `export dummyFrame := Frame(self, -1, 0, true, Sequence());` (`expr.d:55`).

So `Z(3,4)`, `hash_t(0)`, `int(uchar(c))`, `char(i)` and `Expr(ZZcell(…))` are
all the same syntax — a type name applied like a function.

### Type identification

`totypesRec` (`type.c:482–636`) runs partition refinement over newly declared
types and merges the indistinguishable ones. Two asymmetries matter, and `foo.d`
is built to show both.

> **Try it.** Compile
>
> ```d
> A := {x:int, y:int};
> B := {x:int, y:int};
> AT := {+ x:int, y:int};
> BT := {+ x:int, y:int};
> f(a:A):int := a.x;
> ```
>
> The header has three struct types, not four:
>
> ```c
> typedef struct A_struct * A;
> typedef struct AT_struct * AT;
> typedef struct BT_struct * BT;
> ```
>
> `B` was merged into `A` — and `f(B(1,2))` type-checks — while `AT` and `BT`,
> identical but tagged, stay distinct (`type.c:537`). That is why `foo.d`
> declares `W`, `WW`, `WWW`, `WWWW` as four separate `tarray(Z)` types, and why
> the file as shipped does not compile: the `tarray(Z)` written inside `U` is a
> *fifth* such type.

The order of declarations affects the outcome, and the comment at
`type.c:496–498` admits it: *"This routine probably has bugs, with the result
that the order of declarations makes a difference."* `Macaulay2/c/foo.d:221–228`
is the test case, and `README:101` gives the resulting rule: **put `or`-type
declarations after the declarations of their component types.**

### Type codes

Type tags are *persistent across compilations*, kept in a GDBM database
`typecode.db` next to the sources (`gettypecode`, `chk.c:311–348`). New types
append the next serial number, and codes are handed out only on demand — in
`foo.d`, only `Y`, `Z` and `WWW` need one, because only they are reachable
through a composite union. An unnamed type that needs a code produces the
warning *"Unnamed type requiring a typecode encountered, such a type is unlikely
to be useful."*

---

## 3. Declarations

D has five ways to bind a name, and they are easy to confuse because none of
them is introduced by a keyword:

| Form | Meaning |
| --- | --- |
| `x := e` | define `x`, taking its type from `e` |
| `x : T` | declare, without defining — functions only |
| `f(a:T, b:U):R := e` | define a function; the return type is **required** |
| `f ::= e` | define a macro; nothing is emitted |
| `(x:T) op (y:U) : R := e` | define an operator, prefix or infix |

`import` may precede any of them and `export` all but `x : T`, where it gives
*"not a function or type"*; `threadLocal` applies to variables. Each form is
covered below.

### `x := e`

`chkdefinition` (`chk.c:1487–1726`). If the left side's type is still deferred it
adopts the right side's type; otherwise `subtype(rtype,ltype)` must hold. If the
inferred type turns out to be `Type`, the definition is a **type** definition and
the type is named after the symbol (`chk.c:1632–1647`). That is the whole of D's
type-declaration syntax: there is no `type` keyword. `X := {x:int, y:int}` is an
ordinary `:=` whose right-hand side happens to be a type.

Redefinition gives *"symbol being redefined"* plus *"here is the previous
definition"*.

### `x : T` — declaration without definition

`chkcolon` (`chk.c:2252–2269`). **Only legal for function types**, where it
records a forward declaration; anything else gives *"declaration without
definition"*. There is a stub acknowledging the gap:

```c
if (israwtype(t)) {
  /* eventually we'd like to allow raw types to be initialized to zero by a declaration without a definition */
}
```

This is how mutual recursion within a file is written — `evaluate.d:42–43`:

```d
eval(c:Code):Expr;
applyEE(f:Expr,e:Expr):Expr;
```

While a forward declaration is outstanding, assigning to the name is an error
(`perform`, `chk.c:61–68`): *"assignment while previous deferred definition
active"*.

At end of compilation `checkfordeferredsymbols` (`dictionary.c:171–186`) reports
*"symbol never defined nor declared"*, *"symbol never defined"*, or *"symbol
never declared"*.

### `f ::= e` — macros

`chkcoloncolonequal` (`chk.c:2271–2323`). Macro variables are expanded at every
use; macro functions are expanded by substitution, with each already-checked
argument wrapped so it is not re-checked. Macro functions overload on argument
types like real functions, and have no declared return type — it is inferred.
**No C function is emitted.**

```d
export ERROR ::= -1;                                             -- stdio0.d:5
export NULL ::= null();                                          -- expr.d:45
export ! (x:bool) ::= Ccode(bool,"(!(",x,"))");                   -- arithmetic.d:30
export load(x:atomicField) ::= Ccode(int, "load_Field(",x,")");   -- atomic.d:16
```

`README:262–263` warns that only simple macros export cleanly, because of
printing problems in `dprint()`.

Contrast `stdio0.d:12`: `export STDERR:int:=2;` is deliberately *not* a macro,
with the comment "will be modified in webapp mode" — a macro cannot be assigned
to.

> **Try it.** Three of `foo.d`'s first four lines are three different kinds of
> definition, and the generated C tells them apart:
>
> ```c
> static char b;      /* b := true      — local to the file      */
> int foo_c;          /* export c := 345 — no `static`, prefixed */
> static int d;
> ```
>
> The macro `(x:int) + (y:int) ::= …` produces no function whatsoever; it is
> spliced at each use, so `d := 2 + 2` compiles to `d = (2 + 2);`. Now delete
> the macro line and recompile:
>
> ```
> nomacro.d:3:7: error: not a function or type
> nomacro.d:3:0: error: symbol never declared
> ```
>
> `+` is not part of the language. Interpreter code gets it from
> `arithmetic.d`, via `use`.

### `export`, `import`, `threadLocal`, `constant`, `const`

All of the first four lex as one token (`EXPORT`), and are told apart later by
the symbol's text (`chk.c:1403–1447`). Since `EXPORT` binds tighter than `:=`,
`export x := e` parses as `(export x) := e`.

- **`export`** — sets `export_F`, recomputes the C name with a package prefix,
  and pushes the symbol onto the package's export list, whence the `.sig` file.
- **`import`** — same, but declares that the definition lives elsewhere (another
  package, or hand-written C) and emits none. Three usable shapes:
  `import Parse(text:string):xmlNodeOrNull;` (`xml.d:16`),
  `import gbTrace:int;` (`M2.d:118`),
  `import threadLocal interruptedFlag:atomicField;` (`interrupts.d:12`).
- **`threadLocal`** — see below.
- **`constant`** — **does not work.** It is registered as a reserved word
  (`grammar.y:354`) but `chklhs` compares against the string `"const"`, which
  never matches `"constant"`, so it silently falls through and is misparsed:
  `constant x := 1;` gives *"function definition without return type"* and
  *"symbol never declared"*.
- **`const`** — is *not* a reserved word, so `const x := 1;` is a plain syntax
  error. The `const_F` machinery in `chk.c:1410` and `cprint.c:467` is reachable
  only from compiler-internal construction. `const` is in fact used as an
  ordinary *function* name, `M2.d:24`, under the comment "teach the language
  about \"const\", sigh".

Codegen (`cprintdefine`, `cprint.c:431–489`): exported and imported symbols get
`extern` in the header and no storage class in the body; purely local globals get
`static`, as do non-exported functions.

`export` chains, so one object can have two exported names — `expr.d:89–92`:

```d
export globalDictionary :=
export Macaulay2Dictionary := Dictionary(nextHash(), …);
```

### `threadLocal`

Sets `threadLocal_F`; the work is in `chkdefinition` (`chk.c:1607–1705`). The
type must be a pointer type, `int`, `bool`, a union, or an integer type whose C
name is on a hard-coded whitelist (`unsigned int`, `volatile int`,
`volatile bool`, `char`, `signed char`, `unsigned char`, `short`,
`unsigned short`, `hash_t`). Otherwise: *"thread local variable not valid integer
type"* or *"thread local variable not pointer or integer type"*.

Two strategies:

- `compilerThreadLocal` — a plain variable plus `GC_add_roots(&x, …)` when the
  type is not atomic memory.
- `pthreadThreadLocal` (the default) — declares an `int <name>_id`, registers it
  with `TS_Add_ThreadLocal`, and rewrites every *read* into
  `(*((T*)TS_Get_Local(x_id)))` (`cprint.c:70–81`).

Each initializer becomes its own generated void function appended to
`<pkg>__thread_prepare`.

`threadLocal` and `export` compose in **either order**: `export threadLocal
debugLevel := 0;` (`expr.d:17`) and `threadLocal export recursionDepth := 0;`
(`expr.d:21`).

### `header "…"` and `declarations "…"`

Both lex as `HEADER`; they differ in destination.

- **`header`** (`chk.c:2446–2451`) → the body file, `foo-tmp.c`/`.cc`, with a
  position directive. Not propagated.
- **`declarations`** (`chk.c:2490–2495`) → `foo-exports.h`, **and** pushed onto
  the signature, so `use` re-plays it. Use this for `#include`s whose types
  appear in generated declarations.

Both are emitted through `put_unescape` (`cprint.c:700–718`), which expands
`\n \" \b \t \f \r` and passes any other `\X` through as `X`. So `\n` in the D
string becomes a real newline in the generated C — which is a trap when the
string you are emitting is itself a C string literal. Writing

```d
header "static const char *c = \"one\ntwo\";";
```

splits the literal across two lines and the C compiler rejects it. Double the
backslash to get the escape through intact:

```d
header "static const char *c = \"one\\ntwo\";";   -- emits "one\ntwo"
```

Idiom: define a C global in `header`, then `import` it — `expr.d:69–71`:

```d
header "struct atomic_field expr_threadFramesize;";
import threadFramesize:atomicField;
store(threadFramesize, 0);
```

Note that the C side must spell the mangled name; see
[Name mangling](#7-name-mangling).

---

## 4. Statements and control flow

Everything is an expression; a statement is just an expression used for effect.
`has_no_effect` (`chk.c:15–31`) discards pure-value expressions and reports
*"type expression misplaced"* or *"keyword misplaced"* for a bare type or keyword
in statement position.

### Blocks

`(a;b;c)` has the value of `c`. `(a;b;c;)` — trailing semicolon — has type
`void`. These are separate productions (`chkblockn` vs `chkblock`,
`chk.c:180–212`), both opening a new scope. The trailing `;` is load-bearing:
`export flushToken(f:TokenFile):void := (f.nexttoken=NULL; flushInput(f.posFile););`
(`tokens.d:15`).

Local variables are introduced by `:=` and scoped to the enclosing `( … )`.
There is no `local` keyword in D — where you see the word it is either an M2
top-level keyword being registered or a `void` field used as a discriminator
(`parse.d:142`).

### `if`

`chkif` (`chk.c:952–1005`). Condition must be `bool`. With an `else`, both arms
must agree — *"then/else clauses not of same type"* — but `typematch`
(`chk.c:123–132`) treats `returns`, `exits`, and `bad` as compatible with
anything, so `if p then x else return y` is fine.

> **Try it.** `i := if b then 11 else 22;` is an *expression*, and there is no
> C construct for that, so the compiler makes a temporary and jumps around it:
>
> ```c
>   if (b) goto L0_;
>   tmp_ = 22;
>   goto L1_;
>   L0_:;
>   tmp_ = 11;
>   L1_:;
>   i = tmp_;
> ```
>
> Labels and gotos are how *every* control-flow form is lowered — `newlabel()`
> (`chk.c:219–224`) generates `L0_`, `L1_`, … for `if`, `while`, `for`,
> `foreach`, `when`, `&&`, `||`, `new`, `break` and `provide` alike. There is
> no run-time cost to using `if` for its value.

`if` is used freely as an expression in the interpreter:
`o << (x + if x<10 then '0' else 'a'-10)` (`errio.d:20`);
`(if x.thread then enlargeThreadFrame() else globalFrame).values.(…) = y`
(`expr.d:87`).

### `while` and `until`

One production, one token; `chkwhile` (`chk.c:676–719`) tells them apart by the
symbol text. `until a do b` loops while `a` is false. Constant `true`/`false`
conditions are specialised.

The signature D loop idiom is a side-effecting block as the condition —
`tokens.d:31–33`:

```d
     while (
	  if p.dictionary.frameID == frameID then return p.dictionary;
	  p != p.next) do p = p.next;
```

`until` appears only in `lex.d`, for comment skipping.

### `for`

Four forms, all `chkfor` (`chk.c:418–537`). The index is always `int`.

| Form | Meaning |
| --- | --- |
| `for n do e` | repeat `n` times, no index variable |
| `for i to n do e` | `i` = 1, 2, …, n |
| `for i from m to n do e` | `i` = m, m+1, …, n |
| `for i from m to n by s do e` | step `s`; negative `s` counts down |

> **Try it.** **The default lower bound is 1, not 0** (`one__K`, `chk.c:483`).
> Compile the two loops side by side:
>
> ```d
> (x:int) + (y:int) ::= Ccode(int,"(",x," + ",y,")");
> n := 5; tot := 0;
> for i to n do tot = tot + i;
> for j from 0 to n do tot = tot + j;
> ```
>
> ```c
>   i = 1;      /* for i to n     */
>   j = 0;      /* for j from 0 to n */
> ```
>
> A non-constant step generates a runtime sign test; a constant one leaves the
> dead half of `((i > tmp_) && (1 >= 0)) || ((i < tmp_) && (1 < 0))` for the C
> compiler to fold — the bound is evaluated once into a temporary.

`for n do` is easy to misread as a `foreach`: `for a do provide newvarstring(3);`
(`varnets.d:29`), `for length(word.name) do getc(file);` (`lex.d:112`).

### `foreach`

Four forms, `chkforeach` (`chk.c:539–674`):

```d
foreach a in b do c
foreach a at i in b do c
foreach a in b by s do c
foreach a at i in b by s do c
```

`b` must be an `array` or `tarray`. The index `i` is read-only; **`a` is not** —
it is implemented as an alias for the array slot (`setcprintvalue(var,
array_take(arrtmp,indx))`, `chk.c:620`). Hence `README:274–276`:

> warning: assignment to the variable 'a' in these 'foreach' commands replaces
> the entry in the array! Do we want to change this feature?

The two `by` forms are used nowhere in `M2/Macaulay2/d`.

### `when` / `is` / `else`

The most intricate routine in the compiler, `chkwhen` (`chk.c:721–899`). Rules:

1. The scrutinee must be a union type — *"when-clause requires a union type"*.
2. Each case type must be a member — *"type not among those represented by the
   when-clause"*.
3. Without an `else`, **every** member must be covered, else *"missing case"* /
   *"missing cases"* followed by the 1-based indices of the uncovered members.
4. All arms must agree in type — *"type mismatch between branches"*, again
   modulo `returns`/`exits`.

Two codegen strategies, chosen by whether the union is composite:

- `switch (x->type_)` when there are ≥2 non-`null` members, using the persistent
  type codes; `default: invalidTypeTag(…)` is appended unless `-nocasechks`.
- **labels and `goto`** when there is exactly one non-`null` member, because the
  tag may not physically be there.

`null` cases are tested *before* the switch. With no `null` member and checks
enabled, a null guard is emitted anyway.

> **Try it.** `foo`'s `when` is the whole mechanism in one function:
>
> ```c
> static int foo_1(U u){
>   …
>   if (u == 0) invalidNullPointer(__FILE__,__LINE__,-1);
>   switch (u->type_) {;
>     case 2:;
>     y = ((Y)u);
>     tmp__2 = y->a;
>     break;
>     case 1:;
>     z_1 = ((Z)u);
>     tmp__2 = z_1->d;
>     break;
>     case 3:;
>     w = ((WWW)u);
>     tmp__2 = 44;
>     break;
>     default: invalidTypeTag(u->type_,__FILE__,__LINE__,-1);
>     };
>   return tmp__2;
>   }
> ```
>
> The case labels are the persistent type codes from `typecode.db`, and each
> arm is a cast. Recompile with `scc1 -nocasechks foo.d` and both the null
> guard and the `default:` disappear — that is what `-O` does to interpreter
> builds. Now compile the free-union version from
> [Union types](#union-types) instead, and the `switch` is replaced by
> `if (0 == x) goto L1_;` and a chain of labels.

Three syntactic shapes, all real: `is x:T do` binds, `is T do` does not, and the
spelling for the null case is **`is null do`** — not `is null() do`
(`json.d:63`).

The canonical shape is a staircase, and `else` binds to the innermost open
`when` — `boostmath.dd:57–66`:

```d
inverseRegularizedBeta(e:Expr):Expr :=
    when e is s:Sequence do
	when s.0 is p:RRcell do
	    when s.1 is a:RRcell do
		when s.2 is b:RRcell do
		    handleBoostError(inverseRegularizedBeta(p.v, a.v, b.v))
		else WrongArgRR(3)
	    else WrongArgRR(2)
	else WrongArgRR(1)
    else WrongNumArgs(3);
```

Because the nesting is indentation-only, reflowing one of these silently changes
its meaning. `monoid.dd:41–42` has two *identical* consecutive `else` arms — one
per open `if`.

`else nothing` is the idiom for a `when` used as a statement:
`when e is err:Error do ( … ) else nothing;` And a `when` can serve as a loop
condition — `buckets.dd:14`:

```d
while ( when c is null do false is cell:SymbolListCell do (c = cell.next; true) ) do n = n+1;
```

### `return` and `break`

`chkreturn` (`chk.c:1079–1119`): *"return should be used in the code body of a
function"*, *"return takes at most one argument"*, *"return not allowed in this
context"* (inside a `new … do` body), *"return value missing"*.

A non-void function's body value is returned implicitly (`chk.c:1556–1581`); a
mismatch there is *"type mismatch"*, and a missing declared return type is
*"function definition without return type"*.

`chkbreak` (`chk.c:1246–1261`): *"break should be used inside a loop"*,
*"break not allowed in this context"*. Both forms first run any pending
scope-exit code up to the loop or function boundary.

### `new T len n [at i] do … provide x`

`chknewarray` and `chkprovide` (`chk.c:1273–1378`). Allocate `n` elements, then
run the body repeatedly; each `provide x` stores at the current index and
advances. The optional `at i` binds the current index, which — unlike `for` —
**counts from 0**:

```d
mk():Ar := new Ar len 3 at k do provide P(k);   -- k = 0, 1, 2
```

Errors include *"explicit length needed with array type of variable
length"*, *"explicit length not usable with array type of fixed length"*,
*"new array: no values provided by body"*, and *"provide not allowed in this
context"*. `break` and `return` are disabled inside the body.

> **Try it.** `w := new WWW len 2 do provide z;` becomes
>
> ```c
>   tmp__3 = 0;
>   tmp__5 = 2;
>   if (0 > tmp__5) fatalarraylen(tmp__5,"foo.d",21,17);
>   tmp__4 = (WWW) GC_MALLOC(sizeof(struct WWW_struct) + (tmp__5)*sizeof(Z));
>   if (0 == tmp__4) outofmem2((size_t)sizeof(struct WWW_struct) + (tmp__5)*sizeof(Z));
>   tmp__4->type_ = 3;
>   tmp__4->len = tmp__5;
>   if ((tmp__5 == 0)) goto L3_;
>   L2_:;
>   tmp__4->array[tmp__3] = z;
>   if (((++ tmp__3) < tmp__5)) goto L4_;
>   goto L3_;
>   …
> ```
>
> Note the length check, the tag, and above all the loop condition: **the loop
> is bounded by `len`, not by the body.**

That last point has a consequence. `while true do provide 0` is not an infinite
loop — it stops once `len` elements exist, which is the standard padding trick,
`vararray.d:12–19`:

```d
     	  v.ints = new array(int) len 2*i do (
	       foreach c in v.ints do provide c;
	       while true do provide 0
	       );
```

The corollary is that providing *fewer* than `len` items is a silent bug.

A body may `provide` more than once per iteration (`strings.d:14`) and may mutate
as it goes (`strings.d:20–22`):

```d
export reverse(s:string):string := (
	n := length(s);
	new string len n do ( n = n-1 ; provide s.n));
```

### `&&` and `||`

`chkandand` / `chkoror` (`chk.c:905–951`). Both operands must be `bool`, and both
short-circuit via explicit labels and gotos rather than C's operators, so
side-effecting temporaries land in the right place.

### `Ccode` and `lvalue`

`chkCcode` (`chk.c:1007–1033`). The first argument is the result type; each
remaining argument that is a string constant is spliced literally, and every
other argument is compiled to C and its value or temporary spliced in.
`README:300–306` warns it *"cannot be depended on to do the right thing if the C
code contains flow-of-control constructions."*

`lvalue(x)` (`chk.c:2569–2580`) is the identity but errors with *"lvalue
expected"* if `x` is not assignable — needed whenever the C code takes `&`:

```d
export fetch_add(x:atomicField,y:int) ::=
    Ccode(int, "atomic_fetch_add(&(",lvalue(x),").field,",y,")");   -- atomic.d:20
```

Useful shapes seen in practice:

- `Ccode(T, x)` with a single non-string argument is a **reinterpret cast**:
  `Ccode(constcharstarOrNull,x)` (`M2.d:24`),
  `Ccode(atomicField, "*(struct atomic_field *)", ptr)` (`atomic2.d:17`).
- The D value may come *first*: `Ccode(int, cif, "->nargs")` (`ffi.d:646`).
- An anonymous union type as the result: `Ccode(json_tstar or null, "NULL")`
  (`json.d:48`).
- A D function passed to C as a function pointer, via `GC_REGISTER_FINALIZER`
  (`pthread0.d:44–51`).
- Calling a D function from inside a C string by its mangled name
  (`evaluate.d:1626–1629`).

### Operator declarations

`leftOperator N "op"`, `rightOperator N "op"`, `prefixOperator N "op"` act **at
parse time**, priorities 1–10 only. You rarely need them: the usual operators —
`+ * / < > == << ^ & %` and the rest — are already registered by a prelude
`scc1` parses before every file (`readfile.c:196–223`), which is why `foo.d`
can *define* `+` without first *declaring* it. (`-` is not in that prelude; it
is a literal character in the grammar, `grammar.y:34` and `175–176`, so unlike
the others it survives `-nomacros`.) What the prelude does not give
you is any meaning; see [Traps](#9-traps). `chkoperator` (`chk.c:2478–2488`)
deliberately keeps them out of signature files, with the reason:

```
/* operator definitions in a signature file would happen too late, because the parser parses the
   entire source file before "checking" it. */
```

---

## 5. Memory and GC

There is exactly one allocation emitter, `cprintgetmem` (`cprint.c:388–405`), and
the choice between `GC_MALLOC` and `GC_MALLOC_ATOMIC` is made entirely by
`pointer_to_atomic_memory(t)` (`type.c:954–996`):

- **struct / tagged struct** — atomic iff every member is `void`, an
  `atomicType`, or a basic type. Any pointer member makes it non-atomic.
- **union** — never atomic.
- **array / tarray** — atomic iff the element type is a basic type and not a raw
  pointer.
- **`Pointer`** — not atomic; **`atomicPointer`** — atomic.
- **basic type** — atomic.

> **Try it.** `foo.d` allocates three things and gets two different answers:
>
> ```c
>   tmp__6 = (Y) GC_MALLOC_ATOMIC(sizeof(struct Y_struct));            /* ints and a bool */
>   tmp__1 = (Z) GC_MALLOC_ATOMIC(sizeof(struct Z_struct));            /* two ints        */
>   tmp__4 = (WWW) GC_MALLOC(sizeof(struct WWW_struct) + (tmp__5)*sizeof(Z)); /* array of Z */
> ```
>
> Add an array of characters and an array of pointers to see the same split
> under one constructor:
>
> ```d
> Chars := array(char);   -- GC_MALLOC_ATOMIC
> Cells := array(Cell);   -- GC_MALLOC, Cell being a struct
> ```
>
> This is why `string`, which is `array(char)`, is allocated atomically
> throughout the interpreter while `Sequence`, which is `tarray(Expr)`, is not.

A companion predicate `is_atomic_memory(t)` (`type.c:940–952`) answers the
different question "does a *value* of this type contain pointers", and decides
whether a `compilerThreadLocal` variable needs `GC_add_roots`.

Sizing: `sizeof(struct) + n*sizeof(elt)` for variable-length arrays;
`sizeof(*((T)0))` for raw pointer types (`cprint.c:363–386`).

Every string literal is a heap-allocated `array(char)` built at package-init time
with a `memcpy` from the C literal (`chk.c:2157–2160`).

`GCmalloc(T)` (`chkmalloc`, `chk.c:1263–1271`) returns a fresh `T`. Under a
`Pointer` type the memory is cleared by `GC_MALLOC`; under an `atomicPointer`
type it is not.

### Runtime checks

All in `scc-core.c`, each message carrying the *D* source position:

| Check | Handler | Message | Disabled by |
| --- | --- | --- | --- |
| array index | `fatalarrayindex` | `array index %d out of bounds 0 .. %d` | `-noarraychks` |
| `new` length | `fatalarraylen` | `new array length %d less than zero` | `-noarraychks` |
| bad type tag | `invalidTypeTag` | `internal error: unrecognized type code: %d` | `-nocasechks` |
| null in `when` | `invalidNullPointer` | `internal error: invalid null pointer` | `-nocasechks` |
| out of memory | `outofmem2` | `*** out of memory trying to allocate %ld bytes, exiting ***` | never |

---

## 6. Static checks

`error.c` caps errors at 120 and warnings at 240, then aborts. Format is
`file:line:column: message`. `quit()` exits nonzero iff any error occurred, and
`main` refuses to emit C when errors occurred (`scc1.c:328–330`) — note that the
`.sig.tmp` is written *before* that check.

Because D's grammar is so permissive, nearly every mistake surfaces here rather
than as a syntax error. The distinctive messages, grouped by the rule each
reveals, are worth skimming once — they are effectively the language's semantic
specification:

**Types must be types** — *"type expression misplaced"*, *"keyword misplaced"*,
*"not valid type"*, *"invalid type"*, *"part name should be a word"*, *"array
takes a type and an optional length"*, *"array length should be an integer"*,
*"array length should be nonnegative"*, *"expected a pointer type"*, *"untagged
type not usable with other non-null types in a union type"*, *"expected a tagged
pointer type"*.

**Definition discipline** — *"symbol being redefined"*, *"invalid left hand side
of definition"*, *"expected left hand side of := to be a symbol"*, *"declaration
without definition"*, *"redeclaration of function with different type for return
value"*, *"redeclaration"*, *"assignment while previous deferred definition
active"*, *"importing a nonsymbol"*, *"importing a symbol already initialized"*,
*"importing a previously defined symbol"*, *"invalid macro function
definition"*, *"C++ or C keyword used as parameter"*, and — memorably —
*"internal error 22"*, whose source comment reads *"need a better error message
here"*.

**Type agreement** — *"type mismatch"*, *"type mismatch between branches"*,
*"then/else clauses not of same type"*, *"impossible type conversion"*, *"type
conversion requires one argument"*, *"type of argument not among those in the
union"*, *"wrong number of initial values"*, *"wrong type"*, *"too many
arguments"*, *"too few arguments"*, *"unsuitable arguments"* (no overload
matched), *"function definition without return type"*, *"return value missing"*.

**Not yet known** — *"not declared yet"*, *"undefined"*, *"not defined"*, *"not
declared"*.

**Control-flow context** — *"condition should be of type bool"*, *"if-statement
takes 2 or 3 arguments"*, *"when-clause requires a union type"*, *"type not among
those represented by the when-clause"*, *"missing case(s)"*, *"return should be
used in the code body of a function"*, *"break should be used inside a loop"*,
*"provide not allowed in this context"*, *"new array: no values provided by
body"*, *"should be an array or tarray"*, *"lvalue expected"*.

**Packages** — *"undefined package (no *.sig file found)"*, *"signature file
read, but package remains undefined"*, *"circular package dependency"*, *"not a
package"*, *"outside of a package"*, *"invalid operator definition"*.

---

## 7. Name mangling

Three composable transformations, all in `dictionary.c`, applied by
`internsymbol` (`dictionary.c:346–376`).

1. **`totoken()`** (`dictionary.c:258–306`) — alphanumerics pass through
   (`dictionary.c:264`); every other character becomes a word plus `_`:
   `* → star_`, `< → less_`, `+ → plus_`, `- → minus_`, `/ → slash_`,
   `> → greater_`, `= → equal_`, `! → pt_`, `. → period_`, `| → or_`,
   `^ → circ_`, `& → amp_`, `~ → tilde_`, and so on. A leading digit gets a `_`
   prefix. So `+` → `plus_`, `<<` → `less_less_`, `^^` → `circ_circ_`.
   **Underscore is not in the pass-through set** (`dictionary.c:275`): it is
   spelled out like any other punctuation: `my_var` becomes
   `myunderscore_var`, or `us_myunderscore_var` if it is exported from a file
   `us.d` — the package prefix comes from step 2, not this one.
2. **`prefixify()`** (`dictionary.c:323–333`) — applied only to exported and
   imported symbols; prepends the package chain, each component followed by `_`.
   A package literally named `C` is skipped, which is the escape hatch for
   binding to unmangled C symbols.
3. **`uniquify()`** (`dictionary.c:28–35`) — a per-name counter. The first
   occurrence keeps its name; the Nth gets `_<N-1>`. This is what resolves
   overloading and shadowing. Suppressed by `nouniquify_F`, set on function
   parameters so they stay readable.

   The counter is **per file, not per scope**, so an ordinary local can be
   renamed because an unrelated function used the name first: a loop index `k`
   comes out as `k_1` if some earlier function already had a `k`. Parameters
   are exempt, which makes the asymmetry look arbitrary in generated C.

So the pattern is **`package_name`**, with operator characters spelled out and a
numeric suffix on overloads. You need this whenever you write raw C in `header`
or `Ccode`.

> **Try it.** Predict the C names for the last three lines of `foo.d`, then
> check. There are four `foo`s in play — three functions, plus the package
> itself, which is named after the file — and they come out as
>
> ```c
> static int foo_1(U u){ …          /* foo(u:U),      not exported */
> static int foo_2(int x,int y){ …  /* foo(x,y),      not exported */
> int foo_foo(){ …                  /* export foo()                */
> int foo_foo_1(int x){ …           /* export foo(x:int)           */
> ```
>
> Operator names go through `totoken` first: in a file `nm.d`,
> `export (x:int) < (y:int) : bool := true;` becomes
> `char nm_less_(int x,int y)` — note `char` for the `bool` return.

Exceptions: `literal_F` symbols bypass steps 1 and 2 entirely (used for
compiler-generated names and the `<pkg>__prepare` family); keyword symbols get no
C name at all; and `init_dictionary` hard-codes `one_ → "1"`, `zero_ → "0"`,
`true → "1"`, `false → "0"`, `char → "signed char"`.

Type names become `typedef <ctype> <mangled>;` with struct tags
`struct <name>_struct`, or `struct M2_<seqno>` for an anonymous type
(`cprint.c:272–281, 407–429`).

Emission order in `cprinttypes()` (`cprint.c:816–864`) is pointer typedefs,
array bodies, struct bodies, remaining typedefs, function prototypes — with a
caveat at `cprint.c:840`: *"if things are too circular this won't work!"*

### Names you cannot have

Two further mechanisms shape what you are allowed to call things.
`dictionary.c:23–26` marks `this`, `default`, `class` and `mutable` as C++
keywords and rejects them outright as parameter names — `README:71–75` asks for
the list to be extended, because the g++ errors you get otherwise "are
inscrutable". That is why field names throughout `d/` are capitalized
(`Protected`, `Mutable`, `Class`, `Operator`) and why `basic.d:118` has a
parameter named `classs`.

`dictionary.c:10–21` then lists roughly seventy C library and keyword names
(`index`, `stat`, `remove`, `min`, `max`, `erf`, `struct`, …) whose `uniquify`
counters are pre-burned. A D variable named `index` therefore becomes `index_1`
in C, silently, without another `index` anywhere in sight.

---

## 8. Idioms worth knowing

**Function-valued variables, to break package cycles.** Since `use` reads a
`.sig` and the dependency graph must be acyclic, a function defined late is
reached through a mutable variable — `evaluate.d:7–10`:

```d
-- evalprof is not defined until profiler.dd
-- so we use a pointer and populate it later.
dummyevalprof(c:Code):Expr := nullE;
export evalprofpointer := dummyevalprof;
```

with `evalprofpointer = evalprof;` at `profiler.dd:86`. `hashtables.dd:10–20`
does the same for `applyEE`, including a `Ccode(void, "(void)", g)` idiom to
silence unused-parameter warnings.

**Declarations are expressions, and can be assigned to** — `tokens.d:60–61`:

```d
(threadLocal export stopIfError := true) = false;
(threadLocal export debuggingMode := false) = true;
```

Declare-export with one initializer, then immediately assign another.

**No default arguments.** Overloading is used instead — `struct.d:73–75`:

```d
export subarray(v:Sequence,start:int,leng:int):Sequence := (…);
export subarray(v:Sequence,leng:int):Sequence := subarray(v,0,leng);
```

**Operator definitions** come in prefix, infix, and three-argument infix flavours:

```d
export - (x:int) ::= Ccode(int,"(- ",x,")");                  -- arithmetic.d:164
export (s:string) + (t:string) : string := join(s,t);          -- strings.d:16
export (o:file) << (s:string, n:int) : file := o << padto(s,n); -- stdio.d:939
```

`hashtables.dd:967` even overloads `=>` as a macro producing a 2-tuple, so that
hash-table literals can be written in `regex.dd:30–44`.

**`.` does triple duty** — struct field (`t.message`), array index
(`chartypes.c`), and positional access into a sequence (`s.0`, `s.1`, `argv.0`).
A non-identifier index needs parentheses: `v.str.(v.width) = c`.

**Two magic comment conventions.** `-- # typical value: name, Class, Class` is
scraped by the top level to build M2's return-type database (440 occurrences;
the regex is at `m2/typicalvalues.m2:109`). And most files — 50 of 68 — end with an
Emacs `Local Variables:` block carrying its own build command — note that the
target is `.o` even for `.dd` files.

**Dead code to appease the C compiler** — `struct.d:93–96`:

```d
	  fatal("internal error");
	  0	     	       	    -- just to satisfy noisy compilers
```

with a comment above admitting the design is wrong: *"We should have no internal
errors. To fix it, we should have this function … return union types that have to
be tested."*

---

## 9. Traps

1. **`for i to n` starts at 1**, not 0 — while the `at i` index of `new` and
   `foreach` starts at 0. One file shows both: `new Ar len 3 at k` emits
   `k = 0;` and `for k to n` emits `k_1 = 1;`. See
   [`for`](#for).
2. **A `foreach` variable aliases the array slot** — assigning to it mutates the
   array. See [`foreach`](#foreach).
3. **`provide` is bounded by `len`**, so `while true do provide x` terminates,
   and providing too few items fails silently. See
   [Statements and control flow](#4-statements-and-control-flow).
4. **`==` on structs and arrays compares addresses**, not contents. Hence the
   pervasive fast-path idiom `x == y || <deep compare>`, and the fact that
   `===` is a *user-defined* operator with a per-type definition, not a built-in.
5. **`&&` binds tighter than `|`** but `&` binds *tighter* than `&&`, and both
   bind looser than `==`. So the parentheses in `(chartype(c) & DIGIT) != 0`
   (`ctype.d:34`) are load-bearing; without them it parses as
   `chartype(c) & (DIGIT != 0)`.
6. **Nothing is predefined semantically.** Every operator's meaning for every
   type pair is spelled out in `arithmetic.d` as a `::=` macro over `Ccode` —
   163 of them in a 197-line file. There is no implicit promotion: `int + long`
   works only because `arithmetic.d:128` says
   `export (x:int) + (y:long) ::= Ccode(long,"(",x," + ",y,")");`, and a missing
   combination is a compile error, not a coercion.
7. **`^^` is XOR; `^` is `pow`.**
8. **C++ reserved words break the build inscrutably** if used as struct member
   or parameter names — see [Names you cannot have](#names-you-cannot-have).
9. **`when` staircases are indentation-only**, so reflowing one changes its
   meaning.
10. **Fixed-length arrays cannot be used as variable-length ones** — they carry
    no length field.
11. **Two identical tagged types are two types**, however alike; only untagged
    ones are merged. See [Type identification](#type-identification).
12. **`string` is `array(char)`**, so `length(s)`, `s.i`, `s.i = c`, and
    `foreach c in s` all work; but it is a GC object with a `->len` field, which
    is why raw C reads `x->array` and `x->len`.
13. **`constant` does not work and `const` is not a keyword.**

---

## Working on the code

The rest of Grayson's lecture was about the edit/compile/run cycle on the
interpreter itself. His
[exercises](https://github.com/DanGrayson/Internals/blob/master/dan/lecture%202%20exercises.txt)
still work; they are paraphrased here.

**Read the symbol table.** `scc1 -debug` writes `foo.sym`, `foo.out` and
`foo.log`. `foo.sym` lists every symbol with its C name, its type, and its
flags, and is the quickest way to see what the compiler thinks you wrote:

```
foo
      Cname => foo_foo_1
      type => {TYPE[27]:definition => (function ({TYPE[2]:name => int flags< >}) {TYPE[2]:name => int flags< >})}
      value => none
      flags: constant initialized export global
      args => (x)
```

**Find things with tags.** A `TAGS` file is built in `M2/Macaulay2/d` as part of
the build. In Emacs, `M-x tags-search` searches it in a useful order rather than
alphabetically (`C-h f tags-search` for the documentation; `M-x
visit-tags-table` to point at a different one). Search for `"sin"` — with the
quotation marks, which finds where the top-level symbol is *created* — and you
land in `actors3.d`, on a `when` staircase dispatching on `CCcell`, `RRcell`,
`ZZcell` and the rest. That is the shape of nearly every top-level function's
implementation.

**Add a function to the interpreter.** Add a small function to
`M2/Macaulay2/d/actors3.d`, and an entry for it in `M2/Macaulay2/m2/exports.m2`
so the symbol is visible at top level in the `Core` package. Then rebuild:
recompiling the single `.d` file is not enough, because the program has to be
relinked — run `make` in the `Macaulay2/bin` directory of your build tree.

**Run the copy you just built**, in place, so it reads the `.d` files you
modified: navigate to the top of the build directory and run `./M2` rather than
whatever `M2` is on your `PATH`. From Emacs, `C-u f12` gives you a chance to
edit the command line first. Then call your function.

Two follow-ups from the lecture, in increasing order of interest: instead of (or
as well as) exporting the name, add a line to one of the `M2/Macaulay2/m2/*.m2`
files so your function is called when `res 4` is evaluated; and change the D
source so the function returns the cube of its integer argument, finding other
code in `d/*.d` to see how an integer argument arrives from the top level.

`C-x v =` shows what you have changed since the last commit.
