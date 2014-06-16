# How to use git with *Macaulay2*

Install git, if necessary, by getting it here:

* http://git-scm.com/

The follow the instructions in one of the following two sections.

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
  * We'll assume below that your user name is `JohnDoe`.
* Add your ssh key at https://github.com/settings/ssh
* Fork M2 at https://github.com/Macaulay2/M2/fork

Then use one of the following shell commands to get a copy of your copy of the source code of *Macaulay2*:

* `git clone git@github.com:JohnDoe/M2`
* `git clone https://github.com/JohnDoe/M2`

Edit and test your code.  Whenever you want to send your changes to your local copy of M2, issue the following shell commands:

* Add the files with changes to be committed: `git add FILENAME ...`
* Commit the files to your local copy of the repository: `git commit`.  An editor window will pop up in which you should type a message describing the changes, with
  this format:
    * First line is 50 characters or less
    * Then a blank line
    * Remaining text should be wrapped at 72 characters
* Push the commited changes to your fork of M2 at github: `git push`

Repeat at will.  Whenever you want to send your changes to the central Macaulay2 repository, do this in a browser:

* Issue a pull request at https://github.com/JohnDoe/M2/pull/new/master, or find the pull request button on the page of your fork at https://github.com/JohnDoe/M2.

To import the latest changes from the Macaulay2 repository into your repository and try to merge your code with them, use:

* `git pull https://github.com/Macaulay2/M2 master`

To import the latest changes from the Macaulay2 repository into your repository without trying to merge your code with them, use:

* `git fetch https://github.com/DanGrayson/checker`

To display the history of your changes graphically, use this command:

* `gitk`

To show the history of all of your branches and any branches imported from the Macaulay2 repository, use:

* `gitk --all`
