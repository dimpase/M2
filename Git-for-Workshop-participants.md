Each Workshop has a dedicated git repository here on GitHub. The best way to interact with the git repository of the workshop is to clone it and to interact with it through one of the following ways:
1. Using the program [`git`](https://git-scm.com/downloads) via a shell terminal, as explained below.
2. Using [GitHub Desktop](https://desktop.github.com/) via a graphical interface (see the link for help).

Note: on macOS computers, `git` is installed as a part of Xcode with the command `xcode-select --install`.

## Setting up GitHub credentials

Check to see if you have SSH access to GitHub by running the following inside a terminal:

    ssh -T git@github.com

you should see a message like `Hi <username>! You've successfully authenticated, ...`.
If you don't, you might need to check the [key settings](https://github.com/settings/keys) or possibly [generate a new key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent). If you see a big WARNING, read about the fix [here](https://github.blog/2023-03-23-we-updated-our-rsa-ssh-host-key/#what-you-can-do).

## Interacting with the Workshop respository

As a workshop participant, you are part of a GitHub team and this means you can directly interact with the workshop repository (forking the workshop repository is not necessary).

You can clone (i.e. get a local copy of) the workshop repository like this (for Minneapolis 2023 -- adjust as needed).

    git clone git@github.com:Macaulay2/Workshop-2023-Minneapolis.git

Typically, once you join a project you will need to switch to the branch specific to that project:

    git checkout [project-branch]

This is done only once.  From now on, you can update your local copy with whatever is new on the GitHub side using

    git pull --rebase

Later you will use

    git push

to publish any commits (i.e. changes) you made to the main repository.

## Making changes

A *commit* is a small bundle of changes to the state of the repository.  The history of the repository consists of commits and the relations among them.  Each commit has a unique ID which is a hash
value like (e703218f5caf...)

Making changes to the repository takes 3 steps.

1. **add**ing changes to be included in the next commit
2. **commit**ing the changes
3. **push**ing the commit.

At this point we assume you have made some changes like editing a file
or adding a file to the directory you cloned.  You use

    git add FILE

to tell git that you want to include the changes to FILE in your next
commit.  Do this for all new files or changed files you want to
include in the next commit.  As a rule of thumb, one commit should
include all changes that belong to one logical change (i.e. fixing one
bug).  Commits should be as small as possible, but not smaller.

Once you are done adding changes you run

    git commit -m "[short description of the added changes]"

to create a new commit. Each commit includes a text message describing the commit.

Once you have at least one new commit, you can publish it on the main
repository using `git push`.  It will happen that there are some new
changes on the main repository.  You can not push unless you are
up-to-date.  You might need to run `git pull --rebase` or `git pull` first which will merge any
remote changes into your history.  If this happens, the editor will
pop up again and ask you to write/confirm a new merge commit.  After
the merge you will be able to push.

## Slightly more advanced topics

- If you are just making changes to files that are already tracked,
  you can skip the adding phase and run `git commit -a -m "[message]"` which
  automatically adds all changes to known files and creates a new
  commit.

- When you want to push and there are remote changes that don't
  conflict with your changes, you can use

```
    git pull --rebase
```

  to pull those changes and make the history linear with the remote
  changes coming first and yours on top of them.  This will avoid the
  merge commit.

- You can pass the commit message on the command line and skip the
  editor pop-up using the `-m` option:

```
    git commit -m 'This is the commit message'
```

- At the workshop the main repository will be very busy.  That's why
  we plan to work on separate branches.  Please see:
  https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell

- Please also refer to the github tutorial: https://github.com/Macaulay2/M2/wiki/GitHowTo
