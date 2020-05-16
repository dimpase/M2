## Introduction
Sublime Text is a modern text editor for Windows, Mac and Linux. Some key features include
* Fuzzy string searching throughout the editor (autocomplete, opening files, searching for symbols)
* Multiple cursors and selections
* Command palette
* Package manager

## Macaulay2 interface
By installing a few packages, one can obtain an interface to Macaulay2 similar to the official Emacs interface. Syntax highlighting and autocomplete should also work out of the box.

We first need to install Package Control, a package manager. The easiest way is to install it via the **command palette**, whose default keybinding is `Ctrl+Shift+p`. If you start typing "Package Control", there will be an option to install it. To install packages, use the command palette and run the command "Package Control: Install Package" to install new packages. Note that the command palette (and almost everything else in Sublime Text) uses fuzzy string matching, so you don't have to type out the full command. Often a few letters will suffice, e.g. something like "pacoi" should match the option "Package Control: Install Package".

### Terminal in a buffer
To be able to write code on one buffer and send it to another terminal buffer, we will need two packages from Package Control: `SendCode` and `Terminus`. Once these packages are installed, you can open a new buffer and run the command "Terminus: Open default shell in tab (view)" to open a terminal. You may want to use a 2-column layout before doing this (`Alt+Shift+2`). Next, we will configure `SendCode` to work with `Terminus`: run "SendCode: Choose Program" in the command palette, and then choose terminus. 

If you are in a buffer containing source code, the keys `Ctrl+Enter` should now send the line below the cursor to the `Terminus` buffer. Sublime Text will try to guess whether or not you are looking at source code and the syntax from the file name. You can change this by running one of the "Set Syntax: ..." in the command palette.

### Adding the Macaulay2 syntax to Sublime


 



## Links
* [Sublime Text](https://www.sublimetext.com/)