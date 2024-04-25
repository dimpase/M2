This is related to issue #2889.

It would be convenient to have a formal model for the M2 language. This would in particular allow syntax checks of all files in the common library and packages.

Here is the Lark documentation:

https://lark-parser.readthedocs.io/en/stable/

A basic tentative was started in #2893, stuck at a preliminary stage.

This is remotely related to the question of highliting code, as allowed by

https://github.com/mahrud/language-macaulay2

How to use
==========

Here is a sample ipython session:

```
from lark import Lark
with open("macaulay2.lark") as f:
    w = f.read()
m2parser = Lark(w, start='start')
tree = m2parser.parse(open("M2/M2/Macaulay2/packages/DiffAlg.m2").read())
print(tree.pretty())
```

and here the tentative grammar:

```
// this entry point is for a file input
start: (_NEWLINE | expr)*

SYMBOL: WORD

COMMENT: /--[^\n]*/
       | /--.*\n/
       | /-\*.*\*-/
       | ";"

FUNCTION: "sin" | "cos" | "tan" | "abs" | "acos"
        | "agm" | "asin" | "atan" | "atan2"
        | "zeta" | "tanh" | "sqrt" | "sec" | "sech"
        | "erf" | "erfc" | "coth" | "csc" | "eint"

expr: SYMBOL
    | string
    | SIGNED_NUMBER
    | operator_exp
    | command
    | timing
    | assignment
    | lists_and_sequences
    | hash_table
    | branching
    | bool
    | symbols
    | make_function
    | function_call
    | function_def
    | table_access

string: STRING
      | "toString" expr
      | (string "|")+ string

mapping: expr "=>" expr

// functions
typing: ":=" mapping
function_call: (SYMBOL | FUNCTION) "(" expr ("," expr)* ")"
	     | SYMBOL expr
function_def: function_call typing? "->" expr
make_function: (lists_and_sequences|SYMBOL) typing? "->" expr

command: "newPackage" "(" string ("," mapping)* ")" -> new_package
       | "select" "(" lists_and_sequences "," expr ")"
       | "position(" expr ("," expr) ")"
       | "needs" string -> needs_package
       | "method" "(" mapping? ")"
       | "instance" "(" expr "," SYMBOL ")"
       | "class" expr

// operators

unary_pre_op: "-" -> minus
            | "+" -> plus
	    | "#" -> cardinality

unary_post_op: "(*)"
             | "^*"
	     | "^!"
             | "_*"
	     | "_!"
             | "~"
             | "!"

binary_op: "+" -> plus
	 | "-" -> minus
         | "*" -> times
	 | "/" -> div
	 | "//" -> floordiv
         | "**" -> power
	 | "++" -> doubleplus
         | "^"
	 | "^^"
	 | "^**"
         | "<<" | ">>"
         | "<==>" -> equiv
         | "<=="
	 | "<==="
         | "==>"
	 | "===>"
         | "@" | "@@"
         | "&" | "%"
         | "|" | "|-" | "||"
         | ".." | "..<" | ":" | "_"
         | "."

operator_exp: unary_pre_op expr
            | expr unary_post_op
            | expr binary_op expr

// boolean and comparison tests

comparison: expr "==" expr -> equal
          | expr "!=" expr -> unequal
          | expr "===" expr -> strict_equal
          | expr "=!=" expr -> strict_unequal
          | expr "<" expr -> less
          | expr "<=" expr -> less_or_equal
          | expr ">" expr -> greater
          | expr ">=" expr -> greater_or_equal

BOOLEAN: "true" | "false"

bool: bool "and" bool -> and
    | bool "or" bool -> or
    | bool "xor" bool -> xor
    | "not" bool -> not
    | BOOLEAN
    | comparison
    | "all" "(" expr "," expr")" -> all

// new and symbols

// new: "new" hash_table ["of" hash_table] "from" hash_table ":=" (A,B,c) "->" expr

symbols: "global" SYMBOL
       | "local" SYMBOL
       | "symbol" SYMBOL
       | "protect" SYMBOL
       | "threadVariable" SYMBOL

// assignment

assignment: expr "=" expr
          | (expr|SYMBOL) ":=" expr
          | expr "<-" expr

comparison_operator: "?"


// subscripting and object access

accessing: "_" expr -> subscript
         | "." expr -> access_via_key
         | "#" expr? -> length_or_access
         | ".?" expr -> check_for_key
         | "#?" -> check_value
 
table_access: expr accessing

// branching

branching: "if" bool "then" expr ["else" expr]
         | "while" bool ["list" expr] ["do" expr]
         | "for" expr ["from" expr] ["to" expr] ["when" bool] ["list" expr] ["do" expr]
         | "break" expr?
         | "continue" expr?
         | "return" expr?

// exceptions and errors

exception: "error" string
         | "try" expr ["then" expr] ["else" expr]
         | "catch" expr
         | "throw" expr
         | "shield" expr

// timing and alarms

timing: "alarm" NN
      | "time" expr
      | "timing" expr
      | "sleep" NN
      | "nanosleep" NN
      | "elapsedTime" expr
      | "elapsedTiming" expr

// lists, sets, sequences, arrays

bare_sequence: expr ("," expr)*

lists_and_sequences: ("{" bare_sequence "}" | "{" "}")
                   | "(" bare_sequence ")"
                   | "[" bare_sequence "]"
                   | "<|" bare_sequence "|>"
		   | "set" ("{" bare_sequence "}" | "{" "}")

// mapping over hash tables

hash_table: "{" mapping ("," mapping)* "}"

hash_table_operation: "applyValues(" hash_table "," expr ")"
        | "applyKeys(" hash_table "," expr ")"
        | "applyPairs(" hash_table "," expr ")"
        | "scanValues(" hash_table "," expr ")"
        | "scanKeys(" hash_table "," expr ")"
        | "scanPairs(" hash_table "," expr ")"
        | "scan(" hash_table "," expr ")"

// "merge(" A B C ")"
// combine: "combine(" A B C D E")"

_NEWLINE: ( /\r?\n[\t ]*/ | COMMENT )+

%import common.ESCAPED_STRING -> STRING
%import common.SIGNED_NUMBER
%import common.WORD
%import common.LETTER
%import common.NEWLINE
%import common.INT -> NN
%import common.SIGNED_INT -> ZZ
%import common.SIGNED_FLOAT -> RR
%import common.WS
%ignore WS
%ignore COMMENT
```
