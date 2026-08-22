# Avoid these common mistakes

Before diving into the full guide, here are the top things that trip up even experienced Macaulay2 contributors.  If you take a moment to check these out now, then you'll save everyone (including yourself!) time later.

* Target the `development` branch

  The default branch is `stable`, which contains a snapshot of the most recent stable release of Macaulay2.  However, nearly all pull requests should target `development`, which is where code for the next release of Macaulay2 is maintained.  Since it's not the default branch, you will need to manually select it from a drop-down menu when creating a pull request.

  ![image](https://github.com/user-attachments/assets/82e5ab0d-d36a-4b8c-99a3-e88226aadece)


* Add your package to `=distributed-packages`

  All packages should appear in the file [=distributed-files](https://github.com/Macaulay2/M2/blob/development/M2/Macaulay2/packages/%3Ddistributed-packages) in the `M2/Macaulay2/packages` directory.  When submitting a new package, ensure that it is added to the bottom of this file.

* Add a `Keywords` option to `newPackage`

  When submitting a new package, pick a keyword (or keywords) from the headings at the [packages provided with Macaulay2](https://www.macaulay2.com/doc/Macaulay2/share/doc/Macaulay2/Macaulay2Doc/html/_packages_spprovided_spwith_sp__Macaulay2.html) documentation page.  Keywords should appear as a list of strings as the value of the `Keywords` option to `newPackage` at the top of the main file, e.g.,:

  ```m2
  newPackage("MyCoolPackage",
      ...
      Keywords => {"Projective Algebraic Geometry"},
      ...
  ```

* Turn off debugging mode
  
  Make sure that the `DebuggingMode` option to `newPackage` is `false`, or equivalently since `false` is the default, removed entirely.

Keep reading for a step-by-step walkthrough of how to fork the repo, create a new branch, make changes, and open your first PR.

# Making a Pull Request

This section describes the steps for contributing a new package or changes to existing code.  See also [GitHub's official documentation](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).

## If not done previously: fork the Macaulay2 repository on GitHub

In order to open a "[pull request]" (PR) you need to:

0. confirm that you can access GitHub by running `ssh -T git@github.com`. See [this page](https://github.com/Macaulay2/M2/wiki/Git-for-Workshop-participants) if you get authentication errors.
1. create your own "[fork]" of the Macaulay2 repository on GitHub by clicking [here](https://github.com/Macaulay2/M2/fork). At this step it is important that all branches (including `development`) are copied, so **uncheck** the option "Copy the `stable` branch only".
2. create a local "[clone]" of the branch `development` of the new repository on your computer by running:
```
# Replace <USERNAME> with your GitHub username
git clone -b development git@github.com:<USERNAME>/M2.git && cd M2
```
3. finally, check that indeed the `development` has been cloned
```
git branch
```


## If the Macaulay2 repository has already been forked and the `development` branch cloned:
* Suppose that the Macaulay 2 repo is called foo/M2. Change to that directory.
### Move to your own development branch and update it
* Type `git branch` to see your branches. If you see one called `development`, but it is not starred, do 
  * `git switch development`
to change to it. If you do not see a `development` branch, you can get one with 
  * `git fetch development`
  * `git switch development`
* Make sure your development branch is up to date with Macaulay2's, 
  * do this by going to `github.com/USERNAME/M2` (where USERNAME as above is your github name)
  * change to the development branch (drop-down menu with the branch name)
  * then use the drop down "Sync fork" button, to sync with Macaulay2's development branch.
  * on your machine, in the directory "foo/M2", do `git pull` to get the latest version into your computer's local repository.

### Prepare the pull request (These steps are done in the M2 repo on your computer)
* Move your new package(s) or changes to the directory `foo/M2/M2/Macaulay2/packages` where `foo/M2` is the top level of your M2 repository.
  * Use `git add [FILES]`, followed by `git commit -m "some comment about your changes"`), where `FILES` is the list of files you are adding or changing
  * Also, add a line to the file `foo/M2/M2/Macaulay2/packages/=distributed-packages` with the name of each new package on its own line, add newline character too at the end, and `git add M2/Macaulay2/packages/=distributed-packages`, `git commit -m "editing =distributed-packages"`

## At  `github.com/USERNAME/M2`:
### Make the pull request .
* initiate the pull pull request using the dropdown `Contribute` menu and selecting `Open Pull Request`. A new box will open.
* Change the base branch of new pull requests to `development` if necessary.
* Add a title and some comments about the package(s) or changes.
* Click on the `Create Pull Request` button. 

## Go to [`github.com/Macaulay2/M2/pulls`](https://github.com/Macaulay2/M2/pulls).
* Upon creation, your pull request will be given a number and will be available at `https://github.com/Macaulay2/M2/pull/XXXX`, where `XXXX` is the number it was assigned.  Immediately after submitting, it should appear on the top of the *Pull requests* page, but it will begin to move down as other people submit their own pull requests.  To find all of your outstanding pull requests, click the "Author" dropdown menu and select your GitHub username.
* The system will check your spelling and build all the documentation and run all the tests on various systems.  After a few hours, you hopefully will see a ✅ and a message that all checks have passed.  If you see some ❌'s, then at least one of the tests have failed.  The build logs can be overwhelming, but you're encouraged to read through them to see if the failures are due to your changes.  There are a few flaky tests that can cause build failures every once in a while for reasons completely unrelated to your changes.  A Macaulay2 maintainer will restart the builds when that happens.
* Macaulay2 maintainers will review your pull request and either approve it as is or request changes.  Be patient, as this process can take some time.
* If the reviewers request changes, then you have several options:
  * Occassionally, reviewers will provide a suggestion and a "Commit suggestion" button will appear.  If you click this, then a commit will be added to your branch applying the suggestion automatically.
  * You can make changes to your pull request directly in the browser.  Under the "Files changed" tab, click the ⋯ button in the upper-right hand corner of the file you'd like to update and then "Edit file".  Make your changes and then click the "Commit changes..." button to add a commit.
  * If the requested changes are substantial, then it is better to make the changes locally on your machine so that you can test the code before pushing.  Once you've commited any changes (using the same `git add` + `git commit` workflow described above), then `git push` to your fork using the same branch you used when you created the pull request.  The pull request will update automatically.  (A common mistake is to close the first PR and start a second one -- this is unnecessary.)
* After your pull request is approved, then it will be merged into the `development` branch and your changes will appear in the next release of Macaulay2.  Congratulations! 🎉🎉🎉

[fork]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#fork
[pull request]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#pull-request
[clone]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#clone
[branch]: https://docs.github.com/en/get-started/learning-about-github/github-glossary#branch