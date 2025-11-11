#! /usr/bin/env python

import getpass
import shlex
import sys
import time

from enum import Enum
from subprocess import CalledProcessError, CompletedProcess
from subprocess import run as _run

class Color(Enum):
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"

class Prompt(Enum):
    TEXT = "text"
    PASSWORD = "password"

def say(color: Color, msg: str, inline: bool = False) -> None:
    code = color.value if isinstance(color, Color) else "0"

    prefix = "\033[1;" + code + "m[bAIS] "
    suffix = "\033[0m"

    if inline:
        print(prefix + msg + suffix, end=" ", flush=True)
    else:
        print(prefix + msg + suffix)

def ask(prompt: Prompt, msg: str) -> str:
    say(Color.BLUE, msg, inline=True)

    if prompt == Prompt.PASSWORD:
        return getpass.getpass("")

    return input()

def die(msg: str) -> None:
    say(Color.RED, msg)
    sys.exit(1)

def run(cmd: str, die_msg: str | None, check: bool = True, **kwargs) -> CompletedProcess | None:
    try:
        return _run(shlex.split(cmd), check=check, **kwargs)
    except CalledProcessError:
        die_msg(die_msg or f"Command '{cmd}' failed unexpectedly.")

def boom(start: int) -> None:
    assert start > 0

    for i in range(start, 0, -1):
        say(Color.YELLOW, str(i) + "...")
        time.sleep(1)

def probe(disk: str) -> None:
    run(f"partprobe {disk}", die_msg=f"Failed to probe the disk {disk}.")
    time.sleep(1)
