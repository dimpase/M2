# Branches

We have two main branches on GitHub:

* [`development`](https://github.com/Macaulay2/M2/tree/development) -- all pull requests are merged into this branch
* [`master`](https://github.com/Macaulay2/M2/tree/master) -- most recent stable release

(*Note:*  These branch names are under discussion.  See [#1130](https://github.com/Macaulay2/M2/issues/1130).)

The `development` branch will always be ahead of the `master` branch, so any merges are done by fast-fowarding.

Near release time we have a release branch, with name of the form `release-X.Y-branch`, which is occasionally rebased onto `development`.

# Version numbers

The convention for version numbers of Macaulay2 is this:

* **1.YY.MM**: a major release, such as occurs every 6 months (May 15 and November 15), stable, made into binary distributions
* **1.YY.MM.1**: a minor update, with changes people might want, stable, suitable minor updates to binary distributions on certain architectures
* **1.MM.YY-n-gxxxxxxxxxx**:  a development version, with no binary distributions.  The version number is obtained using `git describe --tags --dirty`.

# Release procedure

* Things to do when incrementing the version number to X.Y.Z, say :
   - increment the version number in the file [`VERSION`](https://github.com/Macaulay2/M2/blob/master/M2/VERSION)
   - add an entry to [`distributions/deb/changelog`](https://github.com/Macaulay2/M2/blob/master/M2/distributions/deb/changelog) (*TODO:* Is this still useful?)
   - commit the two files and push upstream

* Things to do when developing a binary release for version X.Y (or version X.Y.Z)
  - make a git branch of the form `release-X.Y-branch` and switch to it

        git checkout -b release-X.Y-branch
  - push it upstream:

        git push -u origin release-X.Y-branch

  - open a draft pull request
  - update the symbols in [`prism.js`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/Style/prism.js), which adds syntax highlighting to the html documentation:

         make -C Macaulay2/editors update-syntax-highlighting

  - M2-emacs and other syntax highlighting files should be updated

  - run `npm install` in `M2/Macaulay2/packages/Style` to make sure that our vendored copy of KaTeX is up to date.

  - update the file [`M2/Macaulay2/packages/Macaulay2Doc/changes.m2`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/Macaulay2Doc/changes.m2) to take the release into account

    - find out how the file [`Macaulay2/m2/exports.m2`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/m2/exports.m2) has changed since the previous release (using `git diff`), and make appropriate entries to document the new symbols and the deleted symbols.

    - find out how the file [`Macaulay2/packages/=distributed-packages`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/=distributed-packages) has changed since the previous release, and make appropriate entries to document the new packages.  See [`Macaulay2/packages/Macaulay2Doc/README`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/Macaulay2Doc/README) for helper code.

    - find out which packages have been featured in articles published by the *Journal of Software for Algebra and Geometry* at https://msp.org/jsag/ since the previous release, and add certification blocks to those packages, using the template in the file [`Macaulay2/packages/CertificationTemplate`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/CertificationTemplate).  The git commit number in the certification should point to a version of the package that is identical with the version provided by the journal.  (If necessary, add commits and merge them in to provide one.)  Also, make appropriate entries to document the newly published and certified packages.
  - periodically rebase the branch onto the `development` branch.  Continue accepting pull requests into the `development` branch.
* When the release is ready, do:
  -  on the branch `release-X.Y-branch`, do:

         git tag release-X.Y
         git push origin release-X.Y

  - mark the pull request as ready and merge it into `development`
  - push the release tag to the `master` branch:
   
         git push origin release-X.Y:master

  - on the web site, update the documentation and version number
  - add the new version number to the [`versions.json`](https://macaulay2.com/doc/versions.json) file on the website.  This is a file that should exist on the webserver in the same directory as the various `Macaulay2-X.Y` subdirectories containing the documentation.  It should contain a JSON object whose elements are key-value pairs corresponding to all of the Macaulay2 versions that have documentation available on the website in decreasing order.  The keys contain how each version will appear in the dropdown version selection menu, and the values contain the corresponding version numbers, e.g.,
    ```js
    {"latest release (1.22)": "1.22", "1.21": "1.21", "1.20": "1.20"}`
    ```
     This is used by [`version-select.js`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/packages/Style/version-select.js) in the `Style` package to create the dropdown menu.

# Checking new releases and distributions

There are some things about a new distribution of Macaulay2 that should be checked manually.  Install the distribution on your system as the ultimate user will and then try:

- **emacs M2 interaction**: Press <kbd>f12</kbd> and verify that Macaulay2 starts.

- **emacs M2 mode**: Visit the file `/tmp/foo.m2` and verify that the buffer is in Macaulay2 mode.

- **emacs Macaulay2 info documentation**: Start the emacs Info documentation reader with <kbd>C</kbd>-<kbd>h</kbd> <kbd>i</kbd> and verify that menu items are present in the node	`(dir)Top` for the various Macaulay2 packages in a section entitled "Macaulay2 and its packages".

- **readline**:  Start M2 in a terminal window and then type the following characters: <kbd>r</kbd><kbd>e</kbd><kbd>s</kbd><kbd>o</kbd><kbd>TAB</kbd>.  The partial word should be completed to `resolution`.  Then press <kbd>C</kbd>-<kbd>a</kbd>. # Verify that the cursor is now at the beginning of the line.

- uncategorized packages should get a keyword:
  ```m2
  select(separate_" " version#"packages", p -> (readPackage p)#Keywords === {"Uncategorized"})
  ```

- check existing keywords for sensibility and near duplicates
  ```m2
  stack sort unique flatten apply(separate_" " version#"packages", p -> (readPackage p)#Keywords)
  ```

- `DebuggingMode` should be turned off in packages:
  ```m2
  select(separate_" " version#"packages", p -> (readPackage p)#DebuggingMode)
  ```

- See whether the documentation looks okay.  Do this both without and with installing a fresh copy of `FirstPackage` and restarting.  Make sure the example output is there.
  ```m2

		i1 : loadPackage "FirstPackage"

		o1 = FirstPackage

		o1 : Package

		i2 : help firstFunction

		o2 = firstFunction
		     *************

		     Description
		     ===========

		     Here we show an example.

		     +--------------------+
		     |i1 : firstFunction 1|
		     |                    |
		     |o1 = Hello World!   |
		     +--------------------+
		     |i2 : firstFunction 0|
		     |                    |
		     |o2 = D'oh!          |
		     +--------------------+

		     Ways to use firstFunction :
		     ===========================

		       * "firstFunction(ZZ)" -- a silly first function

		o2 : DIV
  ```

* see whether <kbd>C</kbd>-<kbd>c</kbd> works in emacs and in a terminal, both for M2 and its subjobs:
  ```m2
		i1 : while true do 1
		  C-c C-cstdio:1:15:(3): error: interrupted

		i12 : run "sleep 10"
		  C-c C-c			<-- interrupted immediately -->
		o12 = 2				<-- right answer

		i2 : run "sleep 10"
		  C-c C-c			<-- too much delay -->
		o2 = 0				<-- wrong answer


		i3 : uninstallPackage "Schubert2"; installPackage "Schubert2"
			...
						<-- wait for it to start running examples:
		--making example results for Riemann-Roch on a curve in file /Users/dan/Library/Application Support/Macaulay2/local/share/doc/Macaulay2/Schubert2/example-output/___Riemann-__Roch_spon_spa_spcurve.out
		ulimit -t 700; ulimit -s 8192; cd /var/folders/40/dy88l5qd361391m_3v2m51bm0000gn/T/M2-69452-0/9-rundir/; /Users/dan/src/M2/github/Macaulay2-M2-clone/M2/BUILD/dan/builds.tmp/mac64.production/M2 --silent --print-width 77 --stop --int --no-readline -q -e 'loadPackage("Schubert2", Reload => true, FileName => "/Users/dan/src/M2/github/Macaulay2-M2-clone/M2/Macaulay2/packages/Schubert2.m2")' <"/var/folders/40/dy88l5qd361391m_3v2m51bm0000gn/T/M2-69452-0/4___Riemann-__Roch_spon_spa_spcurve.m2" >>"/Users/dan/Library/Application Support/Macaulay2/local/share/doc/Macaulay2/Schubert2/example-output/___Riemann-__Roch_spon_spa_spcurve.errors" 2>&1
		  C-c C-c			<-- then interrupt it:
		  				<-- expect it to stop immediately with something like this:
		/Users/dan/Library/Application Support/Macaulay2/local/share/doc/Macaulay2/Schubert2/example-output/___Riemann-__Roch_spon_spa_spcurve.errors:0:1: (output file) error: Macaulay2 exited with return code 2
		/var/folders/40/dy88l5qd361391m_3v2m51bm0000gn/T/M2-69452-0/4___Riemann-__Roch_spon_spa_spcurve.m2:0:1: (input file)
		stdio:4:1:(3): error: subprocess interrupted
  ```

* see whether the `--int` command line option works to suppress `SIGINT` handling:
  ```m2
 		   <-- see whether you can interrupt M2 while it's waiting for input:

		   $ M2 --stop --int
		   i1 : C-c C-c
		   $ echo $?
		   130				<-- right answer

 		   <-- see whether you can interrupt M2 while it's running:

		   $ M2 --stop --int -e 'print hi ; while true do 1'
		     				<-- wait for "hi" to be printed
		   C-c C-c			<-- interrupted immediately -->
		   $ echo $?
		   130				<-- right answer
   ```

* see [`0-final-check-interactive-input-behaviour`](https://github.com/Macaulay2/M2/blob/master/bugs/dan/0-final-check-interactive-input-behaviour) if changes have been made to top level user interaction

* see whether you can interrupt the printing out the following commands, e.g., in emacs with <kbd>C</kbd>-<kbd>c> <kbd>C</kbd>-<kbd>c</kbd>:
  ```m2
  << 1..50000
  1..50000
  ```

* run a benchmark and compare to previous versions to make sure optimization is on:
  ```m2
  benchmark "scan(0..10000,i->i^3)"
  loadPackage "Benchmark"
  runBenchmarks
  ```

* fix bugs

* add test files

* run `ldd M2` or `otool -L M2` in `...your-build-tree.../StagingArea/x86_64-MacOS-10.5/bin/` to see that we don't depend on any of our own sharable libraries (yet), or on any libraries installed in nonstandard locations, such as in `/sw/lib`

* do the same in `...your-build-tree.../StagingArea/x86_64-MacOS-10.5/libexec/Macaulay2/x86_64-MacOS-10.5/` for all the programs we compile and distribute

* check that readline and history and name completion work in an xterm

* look at html documentation 

* look at info documentation

* run M2 without `-q` option and then try `viewHelp` to see if the list of installed packages is up to date

* check for bad links:

		cd  ~/Library/Application\ Support/Macaulay2
			or
		cd ~/.Macaulay2
			and
		find . -name \*.html |xargs html-check-links

* try `viewHelp res`, etc.

* update [`Macaulay2/man/M2.1.in`](https://github.com/Macaulay2/M2/blob/master/M2/Macaulay2/man/M2.1.in)

* check that alarm works or devise an automated test:
  ```m2

		i11 : alarm 4 ; for i from 0 do j = i
		stdio:10:31:(3): error: alarm occurred

		i13 : j

		o13 = 1858410
  ```

* check that `installPackage` works for the user (now, with no symbolic links) and that it creates a documentation database and finds and uses it, e.g.:
  ```m2
	      	i1 : installPackage "Classic"

		   and then:

		i1 : notify=true

		o1 = true

		i2 : loadPackage ("Classic",Reload=>true)
		--opened database: /Users/dan/src/M2/trunk/BUILD/dan/builds.tmp/mac64.production/StagingArea/x86_64-MacOS-10.6/lib/Macaulay2/x86_64-MacOS-10.6/Classic/cache/rawdocumentation-dcba-8.db
		--beginDocumentation: using documentation database, skipping the rest of /Users/dan/Library/Application Support/Macaulay2/local/share/Macaulay2/Classic.m2
		--package "Classic" loaded
		--loaded /Users/dan/Library/Application Support/Macaulay2/local/share/Macaulay2/Classic.m2

		o2 = Classic
  ```
* check that `installPackage "Macaulay2Doc"` works

* try `edit(dim,Module)`, in emacs under X and in emacs in an xterm

* verify that `applicationDirectory()` yields `~/Library/Application Support/Macaulay2/` under Mac OS X and `~/.Macaulay2` under other OSes.  Then verify that if that directory is removed, M2 can still start up (without the `-q` command line option).

* verify that `~/.Macaulay2/README` or `~/Library/Application Support/Macaulay2/README`, if it is deleted, is restored by running M2 without the `-q` option

* run <kbd>M</kbd>-<kbd>x</kbd> `Info-validate` on the info file

* make sure the links in the html documentation work

* run `make -k check` and check the output

* make sure the macos x readme file is up to date

* test SCSCP:
  - Start a server in one M2 process
    ```m2
		 i1 : loadPackage "SCSCP";
		 i2 : startServer();
		 [SCSCP][Server] Listening on :26133
    ```
  - Test the server from another M2 process by computing 1+2 and getting 3 in response:
    ```m2
		 i1 : loadPackage "SCSCP";
		 i2 : s = newConnection "localhost"
		 o2 = SCSCP Connection to Macaulay2 (0.1) on localhost:26133
		 i3 : s <== openMath 1+2
		 o3 = 3
    ```
  - Try to stop the server by typing a Ctrl-C on the first process
    ```m2
		 [SCSCP][Server] Listening on :26133
		 [SCSCP][Server] Incoming connection. Forking.
		   C-c C-c
		   currentString:1:16:(3):[15]: error: before eval: --backtrace update-- 
    ```
* Occasionally test all the packages that cache their example output.  This can be done on a machine where you have installed all the prerequisite external programs for those packages (see `../../M2/INSTALL`, "Rerunning the package examples"), with a fresh build tree, by adding the command line option RerunExamples=true to the `make` command.  If you forgot to do that the first time around, you can first clean the packages with `make clean-packages` in the `M2/Macaulay2/packages` directory of the build tree.