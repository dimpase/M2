# How to use git with *Macaulay2*

## For non-package-developers

To get the source code of Macaulay2 if you are not a package developer, one "clones" our git repository with one of the following shell commands:

* `git clone git@github.com:Macaulay2/M2`
* `git clone https://github.com/Macaulay2/M2`

The source code will appear in a directory called `M2`, which you may rename if you wish.  In that directory you can find the following items of interest:

* Source code for the package Foo: the file `M2/Macaulay2/packages/Foo.m2` and possibly the directory `M2/Macaulay2/packages/Foo/` and its contents.
* Instructions for building *Macaulay2*: `M2/INSTALL`

## For package developers

Start by "forking" the Macaulay2 repository, by following the following steps in a browser.

* Create a github account at https://github.com/
  * We'll assume here that your user name is `JohnDoe`.
* Add your ssh key at https://github.com/settings/ssh
* Fork M2 at https://github.com/Macaulay2/M2/fork

Then use one of the following shell commands to get a copy of your copy of the source code of *Macaulay2*:

* `git clone git@github.com:JohnDoe/M2`
* `git clone https://github.com/JohnDoe/M2`
