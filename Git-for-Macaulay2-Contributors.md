There are two reasons you may wish to download the source code of *Macaulay2*: you may
have a machine for which we have not distributed a recently compiled version of *Macaulay2*,
and thus you want to compile it yourself; you may want to propose a change to *Macaulay2*, such
as adding a new package, modifying an existing package, or modifying some other part of the source
code of *Macaulay2*, such as the interpreter written in the D language, or the engine, written
in C++.  We distinguish those two cases below.

You may also wish to download the files in a workshop repository and modify them.  Eventually we'll
write a third section to cover that case, but for now, please refer to [Git-Info](https://github.com/Macaulay2/Workshop-2018-Madison/wiki/Git-Info).

The source code of *Macaulay2* is stored in a *git repository*, hosted on the web site *GitHub*, and downloaded
with the aid of the command line program *git*.  Install git, if necessary, by getting it here:

* http://git-scm.com/

Then follow the instructions in one of the following two sections.

## For those who want the source code but don't intend to propose changes

To get the source code of Macaulay2 if you are not a package developer, one "clones" our git repository with the following shell command:

* `git clone https://github.com/Macaulay2/M2`

The source code will appear in a directory called `M2`, which you may rename if you wish.  In that directory you can find the following items of interest:

* The source code for the package Foo: the file `M2/Macaulay2/packages/Foo.m2` and possibly the directory `M2/Macaulay2/packages/Foo/` and its contents.
* The instructions for building *Macaulay2*: `M2/INSTALL`

## For those who want the source code and intend to propose changes

Start by "forking" the Macaulay2 repository, by following the following steps in a browser.

* Create a github account at https://github.com/ and log in to it.
  * We'll assume below that your user name is `JohnDoe`.
* Add your ssh key at https://github.com/settings/ssh
* Fork M2 at https://github.com/Macaulay2/M2/fork

Tell git what your name and email address are, for correct labelling of your updates, with shell commands like the following, except
that the name and email address are replaced by yours.

  * `git config --global user.name "John Doe"`
  * `git config --global user.email johndoe@example.com`

Then use the following shell command to get a copy of your copy of the source code of *Macaulay2*:

* `git clone git@github.com:JohnDoe/M2`

Now build Macaulay2 according to the instructions in `M2/INSTALL` and use the result in the following steps.

Edit and test your code.  Whenever you want to send your changes to your local copy of M2, proceed as follows:
* Review the status of your files with
  * `git status`
* Review your changes, if necessary, with `git diff`
* Add the files whose changes are to be committed with `git add FILENAME ...`
* Commit the files to your local copy of the repository:
  * Issue the command `git commit`
  * An editor window will pop up in which you should type a message describing the changes, with this format:
    * First line is 50 characters or less
    * Then a blank line
    * Remaining text should be wrapped at 72 characters
* An alternative to the two steps above, if you are ready to commit all the files that you have changed, is `git commit -a`
* Push the commited changes to your fork of M2 at github: `git push`

Repeat at will.  Whenever you want to send your changes to the central Macaulay2 repository, do this in a browser:

* If you are submitting a new package, remember to add its name to the end of the list in the file `M2/Macaulay2/packages/=distributed-packages`.
* Submit a pull request at https://github.com/USERNAME/M2/pull/new/BRANCHNAME, or find the pull request button on the page of your fork at https://github.com/USERNAME/M2.  The pull request should be directed toward our branch named "master" or "development".
* After submitting your pull request, push no further commits to your branch, so we can have a chance to review your submission.  Once the review is done, comments about your code will be posted on github, and requested changes are easily submitted by committing them to your branch.  Once you finish addressing our comments, let us know by adding a comment, and we'll repeat the process until your code is accepted and "pulled".

To import the latest changes from the Macaulay2 repository into your repository and try to merge your code with them, use:

* `git pull https://github.com/Macaulay2/M2 master`

To import the latest changes from the Macaulay2 repository into your repository without trying to merge your code with them, use:

* `git fetch https://github.com/Macaulay2/M2 master`

To display the history of your changes graphically, use this command:

* `gitk`

To show the history of all of your branches and any branches imported from the Macaulay2 repository, use:

* `gitk --all`

Other links:

* Learn all about how to use git by reading the book at http://git-scm.com/book.
* Magit, a useful emacs mode for performing many of the operations above: https://github.com/magit/magit.
* Learn git by trying it out on someone else's machine: https://try.github.io
