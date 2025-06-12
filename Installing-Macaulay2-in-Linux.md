# APT-based distributions

Debian and its derivatives use the `apt` package manager.  Macaulay2 has been available in the official Debian repositories since 2020, so you may install it using

```
sudo apt install macaulay2
```

Unless you are running Debian unstable or testing, this will likely be a slightly out-of-date version.  The Macaulay2 developers host packages for the latest version of Macaulay2 in third-party repositories.

## Ubuntu
Macaulay2 packages are available for all supported releases of Ubuntu (currently 22.04, 24.04, 24.10, and 24.05).  Run the following:

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
sudo apt install debian-keyring
sudo apt update
sudo apt install macaulay2
```

# RPM-based distributions

Packages for RPM-based distributions are hosted on the Macaulay2 website.  You should download and install two packages:  a "common" package containing the architecture-independent files (such as the Macaulay2 language code and documentation), and a package containing the architecture-dependent files like the M2 executable.


### Macaulay2 1.25.06

| Distribution | Package |
| --- | --- |
| Common (required for all distributions) | [Macaulay2-1.25.06-1.common.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.06-1.common.rpm) |
| Fedora 40 | [Macaulay2-1.25.06-1.x86_64-Linux-Fedora-40.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.06-1.x86_64-Linux-Fedora-40.rpm) |
| Fedora 41 | [Macaulay2-1.25.06-1.x86_64-Linux-Fedora-41.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.06-1.x86_64-Linux-Fedora-41.rpm) |
| Fedora 42 | [Macaulay2-1.25.06-1.x86_64-Linux-Fedora-42.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.06-1.x86_64-Linux-Fedora-42.rpm) |

### Macaulay2 1.25.05

| Distribution | Package |
| --- | --- |
| Common (required for all distributions) | [Macaulay2-1.25.05-1.common.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.05-1.common.rpm) |
| Fedora 40 | [Macaulay2-1.25.05-1.x86_64-Linux-Fedora-40.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.05-1.x86_64-Linux-Fedora-40.rpm) |
| Fedora 41 | [Macaulay2-1.25.05-1.x86_64-Linux-Fedora-41.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.05-1.x86_64-Linux-Fedora-41.rpm) |
| Fedora 42 | [Macaulay2-1.25.05-1.x86_64-Linux-Fedora-42.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.05-1.x86_64-Linux-Fedora-42.rpm)
| Rocky Linux 9.3 | [Macaulay2-1.25.05-1.x86_64-Linux-RockyLinux-9.3.rpm](https://github.com/Macaulay2/M2/releases/download/release-1.25.05/Macaulay2-1.25.05-1.x86_64-Linux-RockyLinux-9.3.rpm)

Then, after downloading these two files, run the following:

```
sudo dnf install Macaulay2-*.rpm
```
For Red Hat Enterprise Linux and compatible distributions like Rocky Linux and AlmaLinux, you may have to enable the [EPEL repository](https://docs.fedoraproject.org/en-US/epel/) to obtain some dependencies.

## Fedora

Macaulay2 is also available in the official Fedora repositories.  The version may be slightly out of date.

```
sudo dnf install Macaulay2
```

# Homebrew on Linux

Macaulay2 bottles are available for x86_64 Linux systems through Homebrew. Follow the instructions on [this page](https://github.com/Macaulay2/homebrew-tap/blob/main/README.md), or simply enter the following to install the Macaulay2 tap and bottle:
```
brew install Macaulay2/tap/M2
```