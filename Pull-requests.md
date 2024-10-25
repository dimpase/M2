Under construction 25 Oct 2024:
This section describes the steps that are needed to contribute code to Macaulay2, i.e. a new package or changes to existing code.

* If you have never done so before, on github, you need to create your own copy ("fork") of the Macaulay2 repository on github:
  * go to `github.com/Macaulay2/M2`
  * click on the drop-down menu arrow button to the right of `Forks` at the top right side of the page
  * create a new fork, unless you already have one.
  * on github switch to the development branch. (You might need to sync it to be the latest, if you have done this before).
* 
* Clone or update the Macaulay2 repository
  * git switch development
  * git fetch
  * git pull
  * git status
  At this point, you have an up to date development branch.
* Switch to the development branch
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