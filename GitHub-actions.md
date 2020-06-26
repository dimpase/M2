**Actions** on Github are tasks that you plan to perform many times (such as building M2 from scratch to test the changes in a new pull request). **Triggers** are Github events (such as a pull request to a particular branch) that will automatically execute the action.

For example, there is now an action in the M2 Github repository called "Build and Test Macaulay2". You can see the **workflow** file for a scheduled run of this action [here](https://github.com/Macaulay2/M2/actions/runs/148535828/workflow) . Some info about this workflow file:
* The first code block describes that the triggers for this action are any of the following:
  * There is a push to the branches master, development, or global (you shouldn't be doing this unless you're Dan or Mike though!)
  * There is a pull request to the branches master or development
  * Scheduled once daily, at 6am EDT. The reason for the daily build and test is that even if M2 code doesn't change, we need to monitor for, for example, a change to one of the external libraries that breaks something in M2.
* The next code blocks for this action execute a "matrix" of two different OS's (MacOS Catalina and Ubuntu 18.04), two different build types (cmake and autotools), and two different compilers (gcc and default), for a total of 8 different builds that are tested every time the action is executed.
  * The **include:** commands are for parts of the build command that change with particular matrix options (for instance on Ubuntu the command "make" is used instead of "gmake").
  * Some tools and libraries are automatically available in the virtual environment, others are installed before building, depending on which OS.
  * Then configure and build commands are defined for autotools versus cmake.
  * Etc.

The purpose of an action like this is that the build commands can be programmed once and then automatically run every time you want to test new code with these OS's and build tools. You "do it once and never think about it again." Also, you don't have the issue where someone says "well, it works on my machine," because this establishes a common standard for what it means for M2 to "work" after additions or modifications.

Of course certain changes like changes to the build system would need to be tested manually / more extensively, but for routine checks this saves a lot of time for people like Dan :)

Caveats:
* It can be difficult to debug the issue based on the automated Github action. Log files are saved and individual config files can be downloaded for each build, but this isn't always enough info in everyone's experience. 
* These particular virtual machines aren't going to catch every potential problem, even on Linux for example, since only Ubuntu 18.04 is tested and the virtual machine installation of this OS may differ from the "standard" distribution. 
* There have been issues with not being able to replicate errors from other machines with the Github builds, and vice versa.


