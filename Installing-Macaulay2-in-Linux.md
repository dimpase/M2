# APT-based distributions (Debian, Ubuntu, etc.)

Debian and its derivatives use the `apt` package manager.  Macaulay2 has been available in the official Debian repositories since 2020, so you may install it using

```
sudo apt install macaulay2
```

Unless you are running Debian unstable or testing, this will likely be a slightly out-of-date version.  The Macaulay2 developers host packages for the latest version of Macaulay2 in third-party repositories.

## Ubuntu
Macaulay2 packages are available for all supported releases of Ubuntu (currently 18.04, 20.04, 22.04, 23.10, and 24.04).  Run the following:

```
sudo add-apt-repository ppa:macaulay2/macaulay2
sudo apt install macaulay2
```

Alternatively, if you would like to try out the latest development version of Macaulay2, run the following:
```
sudo add-apt-repository ppa:profzoom/macaulay2
sudo apt install macaulay2
```

## Debian
The instructions are slightly different depending on which version of Debian you are using.

### Debian stable (Debian 12 "bookworm")
As root, add the following to `/etc/apt/sources.list`:

```
deb [signed-by=/usr/share/keyrings/debian-keyring.gpg] https://people.debian.org/~dtorrance/debian bookworm/
```
Then run:
```
sudo apt update
sudo apt install macaulay2
```

### Debian oldstable (Debian 11 "bullseye")
As root, add the following to `/etc/apt/sources.list`:

```
deb [signed-by=/usr/share/keyrings/debian-maintainers.gpg] https://people.debian.org/~dtorrance/debian bullseye/
```
Then run:
```
sudo apt update
sudo apt install macaulay2
```

# RPM-based distributions

Packages for RPM-based distributions are hosted on the Macaulay2 website.  You should download and install two packages:  a "common" package containing the architecture-independent files (such as the Macaulay2 language code and documentation), and a package containing the architecture-dependent files like the M2 executable.

* common package: https://macaulay2.com/Downloads/Common/Macaulay2-1.24.05-1.common.rpm
* architecture dependent package:
  - (Fedora 40): https://macaulay2.com/Downloads/GNU-Linux/Fedora/Macaulay2-1.24.05-1.x86_64-Linux-fedora-40.rpm
  - (Rocky Linux 9.4): https://macaulay2.com/Downloads/GNU-Linux/Red%20Hat%20Enterprise,%20CentOS,%20Scientific%20Linux/Macaulay2-1.24.05-1.x86_64-Linux-rocky-9.4.rpm

Then, after downloading these two files, run the following:

```
sudo dnf install Macaulay2-*.rpm
```

## Fedora

Macaulay2 is also available in the official Fedora repositories.  The version may be slightly out of date.

```
sudo dnf install Macaulay2
```