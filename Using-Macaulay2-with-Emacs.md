Here are some hints about how to get started editing files with emacs and using Macaulay2
within emacs, aimed at those of you who will be attending a Macaulay2 workshop
but have not used emacs much before.

First of all, you should install both Macaulay2 and emacs on the computer that
you will bring with you to the workshop.  The place to get Macaulay2 is here:

[https://faculty.math.illinois.edu/Macaulay2/Downloads/](https://faculty.math.illinois.edu/Macaulay2/Downloads/)

For Mac OS, there is some additional advice about installing emacs here:

[https://faculty.math.illinois.edu/Macaulay2/Downloads/MacOSX/](https://faculty.math.illinois.edu/Macaulay2/Downloads/MacOSX/)

For other systems, such as Linux, it is usually straightforward to install
emacs.

The more recent your OS and your emacs version, the better.  I am using emacs
version 25.3 with Macaulay2 1.11.

First you should learn how to use emacs.  Start emacs and you will probably get a window
that looks like this:

<img src="https://faculty.math.illinois.edu/Macaulay2/Screenshots/emacs-starting-in-window.png" width="400">

(It will not be satisfactory to run emacs within a terminal -- you really want a windows-aware
version of emacs, so try hard to get one.  Here is what it will look like running in a terminal:

<img src="https://faculty.math.illinois.edu/Macaulay2/Screenshots/emacs-starting-in-terminal.png" width="400">
)​

Click on "Emacs Tutorial" to learn the basic emacs commands and how to type
them.  (Another way to start the tutorial is with C-h t .)  

You will be asked
to type many control characters as well as "meta characters".  Typing a control key is done by
holding down the control key while the desired character key is pressed
(briefly, to avoid repetition).  Similarly, typing a meta key is done by
holding down the meta key while the desired character key is pressed.

One might prefer to make that easy by configuring the keyboard in advance so the useless CAPS LOCK key to
the left of the "A" key can serve as a second CONTROL key, and so the key to the
left of the space bar serves as the META key.  On the Mac, this is done in
System Preferences/Keyboard/Modifier Keys -- the Mac name for META is OPTION.
If you prefer to keep the Mac's
COMMAND key in its position to the left of the space bar, then an alternative is to make the COMMAND key
serve as a META key just in emacs by putting the following code in your file `~/.emacs`:

    (setq mac-command-modifier 'meta)

One may also liberate the option key to do what it does in MacOS (e.g., to
input umlauts using option-U) with this command

    (setq mac-option-modifier nil)

Advice about using Macaulay2 in shells and within emacs is available at the [getting started documentation page
](https://faculty.math.illinois.edu/Macaulay2/doc/Macaulay2-1.11/share/doc/Macaulay2/Macaulay2Doc/html/_getting_spstarted.html).

If you follow the instructions there, you will succeed in arranging it so that
typing simply

    M2

on a command line in a shell window starts up Macaulay2.  This is also the way
you will want to run M2 from within emacs.

By the time you arrive at the workshop, you should be comfortable with editing
text in emacs, deleting words and lines, restoring them, undoing changes,
changing from one buffer to another, and cutting and pasting text from one
buffer to another.  You should also be comfortable with creating Macaulay2
files (with names of the form *.m2), editing them, and sending the commands in
them, line by line, to Macaulay2 for execution.

You should also learn how to read emacs' documentation within emacs, using
"info mode".  Start info mode with C-h i and become expert an navigating its
menus and its info files.