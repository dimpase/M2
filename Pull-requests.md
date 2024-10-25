Under construction 25 Oct 2024:
This section describes the steps that are needed to contribute code to Macaulay2, i.e. a new package or changes to existing code.

# Create a fork of the Macaulay2 repo (if not done previously)
* If you have never done so before, on github, you need to create your own copy ("fork") of the Macaulay2 repository on github:
  * go to `github.com/Macaulay2/M2`
  * Use the drop-down menu arrow button to the right of `Forks` at the top right side of the page
* Now on your computer:
  * clone this repository, e.g. `git clone git@git.com/USERNAME/M2.git`, where USERNAME is your git user name.
  * change directory into the new repository on your computer, and check out the development branch with
    `git checkout development`

# Once you have a development branch on your computer: 
* Make sure your development branch is up to date with Macaulay2', 
  * do this by going to `github.com/USERNAME/M2` (where USERNAME as above is your github name)
  * change to the development branch (drop-down menu with the branch name)
  * then use the drop down "Sync fork" button, to sync with Macaulay2's development branch.
  * on your machine: `git pull` to get the latest version into your computer's local repository.

# Prepare the pull request (These steps are done in the M2 repo on your computer)
* Add a "Keywords" option to the call to `newPackage`, e.g.,

  ```m2
    newPackage("MyPackage",
      ...
      Keywords => {"Foo"},
      ...)
  ```
  You can find a list of existing keywords at the [packages provided with Macaulay2](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_packages_spprovided_spwith_sp__Macaulay2.html) documentation page.
* Make sure that the `DebuggingMode` option to `newPackage` is either removed or set to `false`.
  * 
  * push the changes to your forked M2 repository on github by `git push`

  * Move your new package or changes to the directory `M2/Macaulay2/packages` in your M2 repository.
  * Use `git add [FILES]`, followed by `git commit -m "some comment about your changes"`), where `FILES` is the list of files you are adding or changing
  * Also, add a line to the file `M2/Macaulay2/packages/=distributed-packages` with the name of each new package on its own line, add newline character too at the end, and `git add M2/Macaulay2/packages/=distributed-packages`, `git commit -m "editing =distributed-packages"`

# On the github website  `github.com/USERNAME/M2`
* initiate 
    


  * now push to github: `git push`
  * Now go to your repository on github
    * click on `Contribute`, it should suggest making a pull request.
    * FIll out the info
  
  
* 
* Push your changes on this branch to github (Use `git push`)
* On the github website for your cloned M2 repository, do:
  * Step 1
  * Step 2.




Please change the base branch of new pull requests to `development`.

If you are adding a new package, then please also do the following:
* Add the name of your package to the file [`M2/Macaulay2/packages/=distributed-packages`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/%3Ddistributed-packages).
* Add a "Keywords" option to the call to `newPackage`, e.g.,

  ```m2
    newPackage("MyPackage",
      ...
      Keywords => {"Foo"},
      ...)
  ```
  You can find a list of existing keywords at the [packages provided with Macaulay2](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_packages_spprovided_spwith_sp__Macaulay2.html) documentation page.
* Make sure that the `DebuggingMode` option to `newPackage` is either removed or set to `false`.