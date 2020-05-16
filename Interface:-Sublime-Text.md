## Introduction
Sublime Text is a modern text editor for Windows, Mac and Linux. Some key features include
* Fuzzy string searching throughout the editor (autocomplete, opening files, searching for symbols)
* Multiple cursors and selections
* Command palette
* Package manager

## Macaulay2 interface
By installing a few packages, one can obtain an interface to Macaulay2 similar to the official Emacs interface. Syntax highlighting and autocomplete should also work out of the box. _The following instructions are specific to Linux, but should work with minor changes on Windows and Mac_

We first need to install Package Control, a package manager. The easiest way is to install it via the **command palette**, whose default keybinding is `Ctrl+Shift+p`. If you start typing `Package Control`, there will be an option to install it. To install packages, use the command palette and run the command `Package Control: Install Package` to install new packages. Note that the command palette (and almost everything else in Sublime Text) uses fuzzy string matching, so you don't have to type out the full command. Often a few letters will suffice, e.g. something like `pacoi` should match the option `Package Control: Install Package`.

### Terminal in a buffer
To be able to write code on one buffer and send it to another terminal buffer, we will need two packages from Package Control: `SendCode` and `Terminus`. Once these packages are installed, you can open a new buffer and run the command `Terminus: Open default shell in tab (view)` to open a terminal. You may want to use a 2-column layout before doing this (`Alt+Shift+2`). Next, we will configure `SendCode` to work with `Terminus`: run `SendCode: Choose Program` in the command palette, and then choose `Terminus`. 

If you are in a buffer containing source code, the keys `Ctrl+Enter` should now send the line below the cursor to the `Terminus` buffer. Sublime Text will try to guess whether or not you are looking at source code from the file name. You can change this by running one of the `Set Syntax: ...` commands in the command palette.

### Adding the Macaulay2 syntax to Sublime
The Macaulay2 syntax files are not available yet on the official package manager. To install them manually, go to Sublime Text's package directory and clone the [this repository.](https://github.com/haerski/st3)
```bash
cd ~/.config/sublime-text-3/Packages
git clone https://github.com/haerski/st3.git
```
Restart Sublime Text, and the Macaulay2 syntax should be installed and loaded automatically when a `.m2` file is opened. Alternatively, you can force the use of the M2 syntax by running "Set Syntax: Macaulay2" in the command palette. If you open a `Terminus` buffer and run M2 on it, you should be able to send lines of M2 code to the interpreter.

### Wide terminal window
In the Emacs interface, the Macaulay2 interpreter is run in a seemingly infinitely wide terminal buffer, and wide output can be viewed by scrolling horizontally. By default, `Terminus` buffers in Sublime Text are only as wide as the window, and long output will be wrapped. Because of this, very wide Nets look particularly bad.

If you want to have a wider terminal with horizontal scroll, you can install a custom version of Terminus. First, uninstall the old Terminus from Package Control by running `Package Control: Remove Package` in the command palette, and then choose `Terminus`. Then clone [this fork of `Terminus`](https://github.com/haerski/Terminus)
```bash
cd ~/.config/sublime-text-3/Packages
git clone https://github.com/haerski/Terminus.git
```
Restart Sublime Text. After the restart, Package Control may complain about missing dependencies. If this is the case, restart again and Package Control will take care of everything in the next restart. The command `Terminus: Open default shell in tab (view)` should now create a very wide buffer.

### Other useful packages
* `Origami`: create custom window layouts
* `SnippetMaker`: quickly create Tab-completable snippets

### Issues


## Links
* [Sublime Text](https://www.sublimetext.com/)
* [Package Control](https://packagecontrol.io/)