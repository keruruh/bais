# bAIS - basic Arch Install Script

Welcome to **bAIS**, *yet another* custom [Arch Linux][arch_home] installation script!

I made this to simplify the repetitive setup process that follows every fresh Arch Linux install.
Unlike [Archinstall][archinstall] however, **bAIS** is much more simpler. It's designed to be a
starting point which you can freely modify and break however you like to match your own preferences
or workflow.

## Configuration

All configuration is done through the `config.py` file. You should review and adjust the variables
to fit your setup before running the script. This script does **NOT** install any [DE][de] or
[WM][wm] by default, it just configures a basic system and reboots to a fresh Arch Linux install.

## Usage

1. Boot into the Arch Linux installation medium.
2. Ensure you have internet connection.
3. Download and extract the repository.
4. Run the `bais.py` script file.

Simply put, run:

``` bash
curl --location --remote-name https://github.com/keruruh/bais/archive/main.zip
bsdtar -xvf main.zip

cd bais-main/
chmod +x bais.py bais/*.py

python bais.py
```

**Note**: bAIS requires Python 3.8 or later. The Arch Linux installation medium [includes][pkglist]
Python 3 by default.

[arch_home]: https://archlinux.org/ "Arch Linux Homepage"
[archinstall]: https://wiki.archlinux.org/title/Archinstall "Archinstall Wiki"
[de]: https://wiki.archlinux.org/title/Desktop_environment "Desktop Environment Wiki"
[wm]: https://wiki.archlinux.org/title/Window_manager "Window Manager Wiki"
[pkglist]: https://geo.mirror.pkgbuild.com/iso/latest/arch/pkglist.x86_64.txt "Package List"
