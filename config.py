DISK = "/dev/sda"

# Choose from either "x11" or "wayland".
DISPLAY_PROTOCOL = "x11"

# The following values are in GiB.
# You can set SWAP_SIZE to 0 to disable the swap partition altogether.
EFI_SIZE = 1
SWAP_SIZE = 4

USERNAME = "user"
HOSTNAME = "arch"

KEYMAP = "us"
LOCALE = "en_US.UTF-8"
TIMEZONE = "Europe/Madrid"

BOOTLOADER_NAME = "Arch Linux"
BOOTLOADER_TIMEOUT = 10

# Basic list of packages to be installed in the system. All packages listed here
# are technically optional, the only required ones are hard-coded in the script
# when Pacstrap is called.
BASIC_PACKAGES = [
    "ly",
    "sudo",

    "dhcpcd",
    "iwd",
    "networkmanager",
    "ufw",

    "bluez",
    "bluez-utils",
    "pipewire",
    "wireplumber",

    "xdg-desktop-portal",
    "xdg-desktop-portal-gtk",
    "xdg-user-dirs",
    "xdg-utils",

    "nerd-fonts",
    "noto-fonts",

    "man-db",
    "man-pages",

    "atool",
    "curl",
    "git",
    "micro",
    "openssh",
    "reflector",
    "rsync",
    "wget",

    "bluetui",
    "brightnessctl",
    "btop",
    "fastfetch",
]

# The following packages are installed using the "--asdeps" argument in Pacman,
# meaning they are marked as (optional) dependencies.
OPTIONAL_PACKAGES = [
    "tar",
    "unrar",
    "unzip",
    "zip",
    "7zip",

    "noto-fonts-cjk",
    "noto-fonts-emoji",
    "noto-fonts-extra",

    "pipewire-alsa",
    "pipewire-audio",
    "pipewire-jack",
    "pipewire-pulse",
]

# X.Org-specific packages.
XORG_PACKAGES = [
    "xorg-server",
    "xorg-xinit",

    "xorg-apps",
    "xclip",
    "xsel",
]

# Wayland-specific packages.
WAYLAND_PACKAGES = [
    "wayland",

    "wl-clipboard",
    "xdg-desktop-portal-wlr",

    "xorg-xlsclients",
    "xorg-xwayland",
    "xwayland-satellite",
]
