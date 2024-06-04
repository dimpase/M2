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