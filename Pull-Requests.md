This section describes the steps for contributing a new package or changes to existing code.

## If not done previously: fork the Macaulay2 repository on GitHub

In order to open a "[pull request]" (PR) you need to:

0. confirm that you can access GitHub by running `ssh -T git@github.com`. See [this page](https://github.com/Macaulay2/M2/wiki/Git-for-Workshop-participants) if you get authentication errors.
1. create your own "[fork]" of the Macaulay2 repository on GitHub by clicking [here](https://github.com/Macaulay2/M2/fork).
2. create a local "[clone]" of the new repository on your computer by running:
```
# Replace <USERNAME> with your GitHub username
git clone git@github.com:<USERNAME>/M2.git && cd M2
```
3. add the original Macaulay2 repository as the remote "[upstream]" by running:
```
git remote add -f -t development -m development upstream git@github.com:Macaulay2/M2.git
```
4. finally, "[checkout]" the development "[branch]" by running:
```
git checkout development
```


## On your computer: 
* Suppose that the Macaulay 2 repo is called foo/M2. Change to that directory.
### Move to your own development branch and update it
* Type git branch to see your branches. If you see one called "development", but it is not starred, do 
  * `git switch development`
to change to it. If you do not see a development branch, you can get one with 
  * `git fetch development`
  * `git switch development`
* Make sure your development branch is up to date with Macaulay2', 
  * do this by going to `github.com/USERNAME/M2` (where USERNAME as above is your github name)
  * change to the development branch (drop-down menu with the branch name)
  * then use the drop down "Sync fork" button, to sync with Macaulay2's development branch.
  * on your machine, in the directory "foo/M2", do `git pull` to get the latest version into your computer's local repository.

### Prepare the pull request (These steps are done in the M2 repo on your computer)
* Add a "Keywords" option to the call to `newPackage`, e.g.,
  ```m2
    newPackage("MyPackage",
      ...
      Keywords => {"Foo"},
      ...)
  ```
  You can find a list of existing keywords at the [packages provided with Macaulay2](https://macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_packages_spprovided_spwith_sp__Macaulay2.html) documentation page.
* Make sure that the `DebuggingMode` option to `newPackage` is either removed or set to `false`.
* Move your new package(s) or changes to the directory `foo/M2/M2/Macaulay2/packages` where `foo/M2` is the top level of your M2 repository.
  * Use `git add [FILES]`, followed by `git commit -m "some comment about your changes"`), where `FILES` is the list of files you are adding or changing
  * Also, add a line to the file `foo/M2/M2/Macaulay2/packages/=distributed-packages` with the name of each new package on its own line, add newline character too at the end, and `git add M2/Macaulay2/packages/=distributed-packages`, `git commit -m "editing =distributed-packages"`

## At  `github.com/USERNAME/M2`:
### Make the pull request .
* initiate the pull pull request using the dropdown `Contribute` menu and selecting `Open Pull Request`. A new box will open.
* Change the base branch of new pull requests to `development` if necessary.
* Add a title and some comments about the package(s) or changes.
* Click on the `Create Pull Request` button. 

## Go to `github.com/Macaulay2/M2/pulls`.
* The system will check your spelling and run all the Documentation and the TESTs on various systems. If errors are found,
fix them. Make the necessary changes to your files on your machine in `foo/M2/M2/Macaulay2/packages`.
  * Do `git add`, `git commit`, and `git push` as above. The system will automatically restart the pull request and the tests.

[fork]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#fork
[pull request]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#pull-request
[clone]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#clone
[checkout]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#checkout
[branch]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#branch
[upstream]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#upstream