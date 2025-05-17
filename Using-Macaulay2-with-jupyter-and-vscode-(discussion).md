I (Mike Stillman) will be meeting with Paul Zinn-Justin and John Cobb at Fields about May 19-20, 2025 (and hopefully with Doug Torrance remotely).
Here we will record what is the "best" way to use jupyter with M2, either in a browser, or through vscode.  Additionally, we will be working on the vscode Macaulay2 extension, as well as nascent Macaulay2 language server, which Doug has started.

We can use this wiki page to record what we do, and to get ideas from others.  

### Issues for us to consider (please add to this list) to improve the installation and usage of the vscode extension, and/or the jupyter M2 kernel/notebook server.

### Notes on installing jupyter

See [gist](https://gist.github.com/agryman/4b652aab5b8c0ba2ead96c647ebbefc3) for notes about installing on MacOS (most of this is relevant for any system). (Note the section on "Disable Line output wrapping" is done automatically now).

After installing homebrew, python in homebrew, M2, here is basically what is to be done.  *todo*: are there other useful packages in python to install into this venv too?

```
mkdir ~/m2-venv
cd ~/m2-venv
python3 -m venv venv
source venv/bin/activate
# or
source ~/m2-venv/venv/bin/activate
# at this point, you can move to another directory
python --version
pip install jupyter jupyterlab
pip install git+https://github.com/d-torrance/Macaulay2-Jupyter-Kernel.git@notebook-7
jupyter kernelspec list
python -m m2_kernel.install
jupyter kernelspec list
```

### Notes on installing vscode Macaulay2 extension


### Notes on working with the M2 LSP (Language server protocol), for use in any editor that supports the protocol, including vscode and emacs.

#### Installation

The current draft of the language server is available from the pull request [#3687](https://github.com/Macaulay2/M2/pull/3687).  One way to obtain it is to run the following from your clone of the Macaulay2 source repository:

```
git fetch https://github.com/d-torrance/M2 lsp
git checkout lsp
```

Then, if `/path/to/M2` is the path to the top directory of your clone of the Macaulay2 source repository, run the following inside Macaulay2 to install the language server:

```m2
installPackage("JSONRPC", FileName => "/path/to/M2/M2/Macaulay2/packages/JSONRPC.m2")
installPackage("LanguageServer", FileName => "/path/to/M2/M2/Macaulay2/packages/LanguageServer.m2")
```
Finally, copy the file `/path/to/M2/M2/Macaulay2/packages/LanguageServer/M2-language-server` to some directory in your PATH.  In the end, the following should work:

```
command -v M2-language-server
```

#### Working with Emacs

#### Working with VS Code
