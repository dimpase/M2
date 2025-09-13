- [APT-based distributions](#apt-based-distributions)
  * [Ubuntu](#ubuntu)
  * [Debian](#debian)
- [RPM-based distributions](#rpm-based-distributions)
  * [Fedora](#fedora)
  * [Red Hat Enterprise Linux](#red-hat-enterprise-linux)
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

First, run the following:

```
sudo apt update
sudo apt install ca-certificates debian-keyring
```

Next, add a line (as root) to the file `/etc/apt/sources.list`.  The particular line is dependent on your version of Debian.

* **stable (Debian 13 "trixie")**
  ```
  deb [signed-by=/usr/share/keyrings/debian-keyring.gpg] https://macaulay2.com/Repositories/Debian trixie/
  ```
* **oldstable (Debian 12 "bookworm")**
  ```
  deb [signed-by=/usr/share/keyrings/debian-keyring.gpg] https://macaulay2.com/Repositories/Debian bookworm/
  ```
* **oldoldstable (Debian 11 "bullseye")**
  ```
  deb [signed-by=/usr/share/keyrings/debian-maintainers.gpg] https://macaulay2.com/Repositories/Debian bullseye/
  ```

Finally, run:
```
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
sudo dnf install wget
sudo wget -P /etc/yum.repos.d/ https://macaulay2.com/Repositories/Fedora/Macaulay2.repo
sudo dnf install Macaulay2
```

See also 

## Red Hat Enterprise Linux

Macaulay2 is not available in the official repositories for RHEL and compatible distributions like Rocky Linux and AlmaLinux.  However, packages are hosted on the [Macaulay2 website](https://macaulay2.com/Repositories/Scientific/).  Run the following:

```
sudo dnf install wget
sudo wget -P /etc/yum.repos.d/ https://macaulay2.com/Repositories/Scientific/Macaulay2.repo
sudo dnf install Macaulay2
```

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