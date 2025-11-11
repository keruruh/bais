#! /usr/bin/env python

import pathlib
import re
import shutil
import tempfile
import time

import config as c

from bais.utils import *

class Base:
    def __init__(self) -> None:
        self.part_prefix = f"{c.DISK}p" if re.search(r"\d$", c.DISK) else c.DISK
        self.root_part_num = 3 if c.SWAP_SIZE > 0 else 2

    def _clear_disk(self) -> None:
        confirm = ask(Prompt.TEXT, f"The disk {c.DISK} will be completely wiped. Continue? (y/N):")

        if not confirm or confirm.lower() != "y":
            die("Script aborted by the user.")

        say(Color.YELLOW, "Clearing the disk in...")
        boom(3)

        run(f"sgdisk --zap-all {c.DISK}")
        probe(c.DISK)

    def _partition_disk(self) -> None:
        say(Color.GREEN, "Partitioning the disk...")

        EFI_GUID = "C12A7328-F81F-11D2-BA4B-00A0C93EC93B"
        SWAP_GUID = "0657FD6D-A4AB-43C4-84E5-0933C84B4F4F"
        ROOT_GUID = "4F68BCE3-E8CD-4DB1-96E7-FBCAF984B709"

        if c.SWAP_SIZE > 0:
            swap_end = c.EFI_SIZE + (c.SWAP_SIZE + 1)

            run(f"""
                parted --script --align optimal {c.DISK} \
                    mklabel gpt \
                    mkpart ESP fat32 0% {c.EFI_SIZE}GiB \
                    mkpart SWAP linux-swap {c.EFI_SIZE}GiB {swap_end}GiB \
                    mkpart ROOT ext4 {swap_end}GiB 100% \
                    type 1 {EFI_GUID} \
                    type 2 {SWAP_GUID} \
                    type 3 {ROOT_GUID}
            """)
        else:
            run(f"""
                parted --script --align optimal {c.DISK} \
                    mklabel gpt \
                    mkpart ESP fat32 0% {c.EFI_SIZE}GiB \
                    mkpart ROOT ext4 {c.EFI_SIZE}GiB 100% \
                    type 1 {EFI_GUID} \
                    type 2 {ROOT_GUID}
            """)

        probe(c.DISK)

    def _format_partitions(self) -> None:
        say(Color.GREEN, "Formatting partitions...")

        run(f"mkfs.ext4 -F -L ROOT {self.part_prefix}{self.root_part_num}")
        run(f"mkfs.fat -F 32 -n ESP {self.part_prefix}1")

        if c.SWAP_SIZE > 0:
            run(f"mkswap --label SWAP {self.part_prefix}2")

    def _mount_partitions(self) -> None:
        say(Color.GREEN, "Mounting partitions...")

        run(f"mount {self.part_prefix}{self.root_part_num} /mnt")
        run(f"mount --mkdir {self.part_prefix}1 /mnt/boot")

        if c.SWAP_SIZE > 0:
            run(f"swapon {self.part_prefix}2")

    def _install_base(self) -> None:
        say(Color.GREEN, "Installing the base system...")

        required_packages = " ".join(["base", "linux", "linux-firmware"])
        basic_packages = " ".join(c.BASIC_PACKAGES)

        run(f"pacstrap /mnt {required_packages} {basic_packages}", die_msg="Pacstrap failed!")

    def _generate_fstab(self) -> None:
        say(Color.GREEN, "Generating fstab...")

        with open("/mnt/etc/fstab", "w", encoding="utf-8") as fstab:
            result = run("genfstab -t PARTUUID /mnt", capture=True, text=True)

            lines = result.stdout.splitlines()
            new_lines = []

            for line in lines:
                if re.search(r"\s/boot(\s|/efi)", line) and (
                    ["fmask=0077", "dmask=0077"] not in line
                ):
                    line = re.sub(r"(defaults|vfat|ext4|xfs)", r"\1,fmask=0077,dmask=0077", line)

                new_lines.append(line)

            fstab.write("\n".join(new_lines) + "\n")

        result = run("mountpoint --quiet /mnt/boot", check=False, capture_output=True)

        if result.returncode == 0:
            run("umount /mnt/boot")

        run(f"mount --options uid=0,gid=0,fmask=0077,dmask=0077 {self.part_prefix}1 /mnt/boot")

    def _set_passwords(self) -> None:
        say(Color.GREEN, "Setting passwords...")

        root_password_file = tempfile.NamedTemporaryFile(mode="w", delete=False)
        user_password_file = tempfile.NamedTemporaryFile(mode="w", delete=False)

        root_password_file.close()
        user_password_file.close()

        pathlib.Path(root_password_file.name).chmod(0o600)
        pathlib.Path(user_password_file.name).chmod(0o600)

        while True:
            root_password = ask(Prompt.PASSWORD, "Enter root password:")
            root_confirm = ask(Prompt.PASSWORD, "Confirm root password:")

            if root_password == root_confirm:
                break

            say(Color.RED, "Passwords do not match! Try again.")

        while True:
            user_password = ask(Prompt.PASSWORD, f"Enter password for '{c.USERNAME}':")
            user_confirm = ask(Prompt.PASSWORD, "Confirm password:")

            if user_password == user_confirm:
                break

            say(Color.RED, "Passwords do not match! Try again.")

        with open(root_password_file.name, "w", encoding="utf-8") as f:
            f.write(root_password)

        with open(user_password_file.name, "w", encoding="utf-8") as f:
            f.write(user_password)

    def _copy_files(self) -> None:
        script_path = pathlib.Path(__file__).parent.parent
        mount_path = "/mnt/bais"

        shutil.copytree(script_path, mount_path, dirs_exist_ok=True)

        for python_file in mount_path.rglob("*.py"):
            python_file.chmod(0o755)

    def run(self) -> None:
        result = run("mount", text=True, capture_output=True)

        if c.DISK in result.stdout:
            die(f"The disk {c.DISK} is currently mounted! Unmount it first.")

        run(f"loadkeys {c.KEYMAP}")
        run(f"timedatectl set-ntp true")

        self._clear_disk()
        self._partition_disk()
        self._format_partitions()
        self._mount_partitions()
        self._install_base()
        self._generate_fstab()
        self._set_passwords()
        self._copy_files()
