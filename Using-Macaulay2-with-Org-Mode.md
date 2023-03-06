[Org Mode](https://orgmode.org/) is an Emacs major mode with many features, including authoring computational notebooks.

To add Macaulay2 support to Org Mode, first install the Emacs package [ob-M2](https://github.com/d-torrance/ob-M2) and make sure that the cons cell `(M2 . t)` is an element of the list `org-babel-load-languages`.  See the [README](https://github.com/d-torrance/ob-M2/blob/master/README.org) for instructions.

Then open a file in Emacs with the `.org` file extension and add a source code block:

```m2
#+BEGIN_SRC M2
  R = QQ[x, y, z, w]
  monomialCurveIdeal(R, {1, 2, 3})
#+END_SRC
```

Then type <kbd>C</kbd>-<kbd>c</kbd> <kbd>C</kbd>-<kbd>c</kbd>.  This will run the code, giving you the result:

```m2
#+RESULTS:
:         2                    2
: ideal (z  - y*w, y*z - x*w, y  - x*z)
```
See the Org Mode manual on [Working with Source Code](https://orgmode.org/manual/Working-with-Source-Code.html) for more.

