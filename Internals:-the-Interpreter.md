Subsections:
- [the D language](Internals%3A-the-D-language)

The Macaulay2 interpreter is implemented in the `d` directory. The files in this directory are written in the D language, which is a type-safe intermediate language developed by Dan Grayson specifically for the purpose of implementing the interpreter. This language is translated to C by the `ssc1` translator in the `c` directory, before being compiled to produce the M2 binary.

 Note that there is another language known as the [D language](https://dlang.org/), which is an entirely different project unrelated to Macaulay2.

This code has remained static for many years, and no major changes are planned. Here are all the files, in logical order (meaning later files depend on earlier files), with line counts:

```
     152 arithmetic.d *				     149 basic.d		
      61 atomic.d				     417 convertr.d *
     156 M2.d					     303 common.d		
     231 system.d				     298 util.d			
      72 strings.d				     118 struct.d		
      90 varstrin.d				     188 classes.dd		
      37 strings1.d				      49 buckets.dd		
      45 errio.d				     236 equality.dd		
      45 vararray.d				     887 hashtables.dd *
      61 ctype.d				      54 sets.dd		
     399 nets.d					     259 version.dd *
      84 varnets.d				    1813 evaluate.d *		
      78 interrupts.d				      25 mysqldummy.d		
      44 pthread0.d				     223 pthread.d		
       7 stdiop0.d				    1103 actors.d		
    1512 gmp.d					     733 actors2.dd		
     246 engine.dd				    2110 actors3.d *
      27 xml.d					    1577 actors4.d		
      53 stdio0.d				     178 xmlactors.d		
     506 parse.d *				    2107 actors5.d		
     407 expr.d					      36 actors6.dd		
    1036 stdio.d				       3 threads.dd		
     201 stdiop.d				      47 pari.d			
      52 err.d					      46 flint.d		
     235 gmp1.d					    4365 interface.dd *
     171 tokens.d *				     604 interface2.d *		
      18 getline.d				      39 texmacs.d		
     410 lex.d					     644 interp.dd *
     571 parser.d *				
     821 binding.d *


   26439 total
```

Many of these files implement various aspects of the Macaulay2 language. For example:

* `arithmetic.d` - basic arithmetic operations and types
* `strings.d` - strings
* `varstrin.d` - variable length strings
* `nets.d` - implements nets (2D strings, used for example in printing polynomials so that exponents are on separate lines)
* `varnets.d` - variable size nets
* `gmp.d` - interface with multiprecision arithmetic
* `hashtables.dd` - implementation of top level hash tables
* `interface.dd` - interface to functions in the engine

The main parts of the interpreter are in `parse.d`, `tokens.d`, `parser.d`, `converter.d`, `binding.d`, `evaluate.d`, and `interp.dd`. These files cover the process of tokenizing and parsing input from the user, compiling to interpreter runnable code, and then running the code.

#### `parse.d`
has declarations of tokens and keywords.

#### `parser.d`
is where here parsing actually happens. It has functions to parse tokens.
Prefix of n on function (e.g., unaryop / nunaryop) means whether the function can take arguments or not.

#### `binding.d`
binds variables descending down the parse tree. A new dictionary is created in a function definition for the local variables. Must bind correct values to symbols.
Also sets up all keywords and operators with precedence strength.

In top-level M2, one may type

     help "operators"
     help "precedence of operators"

to learn more about Macaulay2 operators and their precedence.

#### `converter.d`
converts parse tree into code that can be run. Code is pseudo-compiled code the interpreter generates (analogous to bytecode).
`Code` is defined in parse.d.

#### `evaluate.d`
evaluates the code in `eval`. 

#### `interp.dd`
is the top-level read-eval-print-loop.

**Exercise:** Modify the interpreter to add a new binary operator. Make sure you can use it in methods.

**Project:** Rearrange code to be more readable or consistently organized in named files.

**Project:** Add code coverage and profiling features to the M2 language.
