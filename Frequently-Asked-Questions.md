Collections:
- [[FAQ: CMake Build Problems]]


Other questions:
<details>
<summary><code>Too many heap sections: Increase MAXHINCR or MAX_HEAP_SECTS</code></summary>

Try the following:
```m2
GC_INITIAL_HEAP_SIZE=50G M2
```

Probably best to save a few gigabytes of your total RAM size for the system so it doesn't crash.
Also see [#500](https://github.com/Macaulay2/M2/issues/500).
</details>