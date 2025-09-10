## Getting Started

Here are some hints about how to get started using Macaulay2 
within VSCode. First of all, you should install both Macaulay2 and VSCode on the computer that
you will bring with you to the workshop. The place to get Macaulay2 is here:

[https://macaulay2.com/Downloads/](https://macaulay2.com/Downloads/)

and the place to get VSCode is here:

[https://code.visualstudio.com/download](https://code.visualstudio.com/download)

Start VSCode and you see a window that looks like this:
<img width="1079" height="748" alt="image" src="https://github.com/user-attachments/assets/fa27f82b-5721-4311-bd6d-10f264ec1e05" />

It will offer various walkthroughs to get acquainted with VSCode. Perhaps the most important menu are the extensions:
<img width="497" height="461" alt="image" src="https://github.com/user-attachments/assets/10057af5-9afc-47dd-b6e7-460bbcf25654" />

Here, you can search the marketplace for various extensions that will make VSCode smarter. Some that I have installed are Github Copilot (an AI coding helper), Live Share (which allows Google doc style real time collaboration), and GitLens (which lets you view the history of a git repo easily).

## Getting a M2 Extension

If you search "Macaulay2", you will see various options:

<img width="286" height="372" alt="image" src="https://github.com/user-attachments/assets/44ea3450-7c37-4eef-a4f8-ad2a90d7e25a" />

These have all been developed to make VSCode recognize and run Macaulay2 code. To install, click on any of them and hit the install button. However, I recommend doing the following instead.

There is currently an effort to make a better VSCode extension that is not yet on the extensions marketplace. To install it, follow this link:

[https://github.com/Macaulay2/vscode-macaulay2/tree/master/releases](https://github.com/Macaulay2/vscode-macaulay2/tree/master/releases)

This contains some number of vsix files (the file used to vscode extensions). Click on the one with the largest number (and therefore the most recent version) and hit download on the menu along the right hand side:

<img width="899" height="110" alt="image" src="https://github.com/user-attachments/assets/eb3b6188-c644-4669-9f24-65585e9ee4ff" />

This will save a vsix file. Now, to install it, go back to the extensions tab and click the 3 little dots in the upper right corner:

<img width="522" height="373" alt="image" src="https://github.com/user-attachments/assets/304e7002-cebc-4544-b80f-3e5e2c1140fc" />

Click "Install from VSIX..." to open your file browser and navigate to the file you downloaded. Click it and installation is done!


## Using the Macaulay2 Extension 
Here, I will explain how to use the VSCode extension that is under development. Open any macaulay2 file in vscode. Navigate to any line and hit Shift+Enter. This should open up a window with a Macaulay2 terminal:
<img width="1195" height="631" alt="image" src="https://github.com/user-attachments/assets/d118021e-4259-4284-ac93-23a802ac41e5" />

You can change the keybinding by navigating to your extension in the extension tab, hitting the settings button (gear icon) and clicking keyboard shortcuts:
<img width="522" height="479" alt="image" src="https://github.com/user-attachments/assets/d1e43354-5eb1-4fa4-a92a-06fb5983dc8b" />

Currently, the default behavior is to try and pretty print all output with LaTeX like the [Macaulay2Web](https://www.unimelb-macaulay2.cloud.edu.au). If you do not like this, run
``` topLevelMode = Standard ```
at any point to change the output style of Macaulay2 to the standard setting. If you encounter any problems, please feel free to submit an issue on our [github repository](https://github.com/Macaulay2/vscode-macaulay2).

