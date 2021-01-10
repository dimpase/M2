Once Macaulay2 is packaged for Debian, Homebrew, and the Fedora distribution is brought up to date, making binary distributions and maintaining repositories on the Macaulay2 website may become obsolete.

### Debian

Macaulay2 is about to be incorporated into the Debian Linux distribution. 

- Debian package cycle: unstable -> testing -> stable distribution
- Time frame for M2 stable release: summer 2021
- Maintenance tasks after stable release: update new releases, handle bugs in packaging, keep libraries up to date
- Future goal: lib-macaulay2?
- More details about Debian integration [here](https://webwork.piedmont.edu/~dtorrance/slides/m2internals20200626.pdf).

Package maintainer is Doug Torrance. See also [https://salsa.debian.org/science-team/macaulay2](https://salsa.debian.org/science-team/macaulay2).

### Homebrew

Macaulay2 is available as a Homebrew bottle for macOS Catalina or any Linux distribution with brew installed via [mahrud/tap](https://github.com/mahrud/homebrew-tap). To add this tap and install Macaulay2 from a bottle, run:
```
brew tap mahrud/tap
brew install M2
```
