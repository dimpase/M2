[Macaulay2Web](https://www.unimelb-macaulay2.cloud.edu.au/#home) is a web interface to Macaulay2 developed over the past couple years by Paul Zinn-Justin as a fork of InteractiveShell. The basic idea is to provide a terminal interface through a browser to a remote machine running Macaulay2. The current codebase is available on [GitHub](https://github.com/pzinn/Macaulay2Web), which has a detailed README and some current issues. The app can be downloaded and run locally with Docker and Vagrant, but is also currently hosted and running at the link to the website above.

The site should display a prompt to the right of the "Home" page when you first visit. You can set up computations and return to them later, as the site will remember you via cookies. KaTeX and HTML are used for displaying output, and stylized input (try typing ESC a l p h a ESC to get a typeset alpha character) can also be used. This is implemented with a new value `WebApp` of the Macaulay2 global variable `topLevelMode`.

The "Editor" tab on the website allows you to edit longer scripts or upload Macaulay2 code you have locally.

The website has several tutorials, and tutorials can be created and loaded as HTML webpages.





