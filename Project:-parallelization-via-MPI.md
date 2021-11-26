* **Potential advisor/consultant(s):** Anton Leykin
* **Goal:** coarse parallelization using Message Passing Interface (MPI)
* **Current status:** available! (some basic functionality has been implemented already)
* **Macaulay2 skill level:** intermediate (some C++ experience is a plus, but not necessary)
* **Mathematical experience:** not important (undergraduate+, see "other info") 
* **Reason(s) to participate:** develop a package that uses a handful of core routines (already in place)  
* **Other info:** an ideal contributor would be someone who has an M2 program that (badly!) needs supercomputing power 

## Project Description

MPI is one of the standard universal interfaces that enables distributed computing on supercomputing clusters (or any computer with multiple cores). The basic idea is to launch several M2 processes (e.g., one per node on a distributed network) and provide an easy mechanism to distribute tasks by exchanging messages between the processes.

***

[This branch](https://github.com/antonleykin/M2/tree/MPI)
contains some preliminary work:

* Outline of master-worker paradigm, how to build, etc.: https://github.com/antonleykin/M2/blob/MPI/M2/Macaulay2/packages/MPI.m2
* Proof of concept program: https://github.com/antonleykin/M2/blob/MPI/M2/Macaulay2/packages/MPI/master-worker-MPI.m2
