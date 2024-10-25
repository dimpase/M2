Under construction 25 Oct 2024:
This section describes the steps that are needed to contribute code to Macaulay2, i.e. a new package or changes to existing code.

# Create a fork of the Macaulay2 repo (if not done previously)
* If you have never done so before, on github, you need to create your own copy ("fork") of the Macaulay2 repository on github:
  * go to `github.com/Macaulay2/M2`
  * Use the drop-down menu arrow button to the right of `Forks` at the top right side of the page
  * Use the pulldown menu to the right of `Code` to copy the commands needed to clone the repository
* Now on your computer:
  * clone this repository, e.g. 
* 
* Clone or update the Macaulay2 repository
  * git switch development
  * git fetch
  * git pull
  * git status
  At this point, you have an up to date development branch.
* On your own machine:
  * Move your package `Foo.m2` to the directory `M2/Macaulay2/packages` in your M2 repository.
  * git add, git commit to add it to your local git repository on your computer
  * make changes to your file(s) if desired, then git add, git commit.
  * Also, add a line to the file `M2/Macaulay2/packages/=distributed-packages` with the name of your package, add newline character too at the end.
  * now push to github: `git push`
  * Now go to your repository on github
    * click on `Contribute`, it should suggest making a pull request.
    * FIll out the info
  
  
* Add and commit your package to this branch (Use `git add [FILES]`, followed by `git commit -m "some comment about your changes"`), where `FILES` is the list of files you adding or changing
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