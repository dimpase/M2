- [APT-based distributions](#apt-based-distributions)
   * [Ubuntu](#ubuntu)
   * [Debian](#debian)
- [RPM-based distributions](#rpm-based-distributions)
   * [Fedora](#fedora)
   * [Red Hat Enterprise Linux](#red-hat-enterprise-linux)
   * [Installing .rpm files without root access](#installing-rpm-files-without-root-access)
- [Arch Linux](#arch-linux)
- [Homebrew on Linux](#homebrew-on-linux)

# APT-based distributions

Debian and its derivatives use the `apt` package manager.  Macaulay2 has been available in the official Debian repositories since 2020, so you may install it using

```
sudo apt install macaulay2
```

Unless you are running Debian unstable or testing, this will likely be a slightly out-of-date version.  The Macaulay2 developers host packages for the latest version of Macaulay2 in third-party repositories.

## Ubuntu
Macaulay2 packages are available for all supported releases of Ubuntu (currently 18.04, 20.04, 22.04, 24.04, 24.10, and 24.05).  Run the following:

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

The directions are slightly different based on your version of Debian.

## unstable ("sid") or testing ("forky")
The latest version of Macaulay2 should appear in the official package repositories for these distributions very shortly after release.

```
sudo apt update
sudo apt install macaulay2
```

This will also work in stable Debian distributions, but it will install an older version of Macaulay2.  It is better to install the packages hosted on the [Macaulay2 website](https://macaulay2.com/Repositories/Debian/index.html):

## stable (Debian 13 "trixie")
```
sudo apt update
sudo apt install ca-certificates debian-keyring wget
sudo wget -P /etc/apt/sources.list.d https://macaulay2.com/Repositories/Debian/trixie/macaulay2.sources
sudo apt update
sudo apt install macaulay2
```

## oldstable (Debian 12 "bookworm")
```
sudo apt update
sudo apt install ca-certificates debian-keyring wget
sudo wget -P /etc/apt/sources.list.d https://macaulay2.com/Repositories/Debian/bookworm/macaulay2.sources
sudo apt update
sudo apt install macaulay2
```

## oldoldstable (Debian 11 "bullseye")
```
sudo apt update
sudo apt install ca-certificates debian-keyring wget
sudo wget -P /etc/apt/sources.list.d https://macaulay2.com/Repositories/Debian/bullseye/macaulay2.sources
sudo apt update
sudo apt install macaulay2
```

# RPM-based distributions

Fedora, Red Hat Enterprise Linux, and RHEL-compatible distributions like Rocky Linux and AlmaLinux use the `dnf` package manager.

## Fedora

Macaulay2 is available in the official Fedora repositories, and may be installed using the following:

```
sudo dnf install Macaulay2
```

The version in the official repositories may be slightly out of date.  To obtain the latest version from the [Macaulay2 website](https://macaulay2.com/Repositories/Fedora/), run the following:

```
curl -O https://macaulay2.com/Repositories/Fedora/Macaulay2.repo
sudo mv Macaulay2.repo /etc/yum.repos.d/
sudo dnf install Macaulay2
```

## Red Hat Enterprise Linux

Macaulay2 is not available in the official repositories for RHEL and compatible distributions like Rocky Linux and AlmaLinux.  However, packages are hosted on the [Macaulay2 website](https://macaulay2.com/Repositories/Scientific/).  Run the following:

```
curl -O https://macaulay2.com/Repositories/Scientific/Macaulay2.repo
sudo mv Macaulay2.repo /etc/yum.repos.d/
sudo dnf install Macaulay2
```

## Installing .rpm files without root access

If you do not have `sudo` privileges on your system, then you may install Macaulay2 by downloading an rpm from the [website](https://macaulay2.com/Repositories/) and installing it into your home directory.

In this example, we assume that you have downloaded the appropriate rpm to `/tmp` and would like to install the files in `~/foo/bar`.  Adjust the filename of the downloaded rpm accordingly.

```
mkdir temp
cd temp
rpm2cpio /tmp/Macaulay2-1.25.06-0.1.m2.el9.x86_64.rpm  | cpio -idm --no-absolute-filenames
mv usr ~/foo/bar/
cd ..
rmdir temp
```

Now start

```
~/foo/bar/bin/M2
```

and use the Macaulay2 command

```m2
setup()
```

to record the location of M2 in your login startup files.

# Arch Linux

Macaulay2 is available in [AUR](https://aur.archlinux.org/packages/macaulay2), the Arch User Repository.  To build and install:

```
git clone https://aur.archlinux.org/macaulay2.git
cd macaulay2
makepkg -s
sudo pacman -U macaulay2-*.pkg.tar.zst
```

# Homebrew on Linux

Macaulay2 bottles are available for x86_64 Linux systems through Homebrew. Follow the instructions on [this page](https://github.com/Macaulay2/homebrew-tap/blob/main/README.md), or simply enter the following to install the Macaulay2 tap and bottle:
```
brew install Macaulay2/tap/M2
```