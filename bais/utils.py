#! /usr/bin/env python

import getpass
import shlex
import sys
import time

from enum import Enum
from subprocess import CalledProcessError, CompletedProcess
from subprocess import run as _run
from typing import Optional

class Color(Enum):
    RED = "31"
    GREEN = "32"
    YELLOW = "33"
    BLUE = "34"

class Prompt(Enum):
    TEXT = "text"
    PASSWORD = "password"

def say(color: Color, message: str, inline: bool = False) -> None:
    code = color.value if isinstance(color, Color) else "0"

    prefix = "\033[1;" + code + "m[bAIS] "
    suffix = "\033[0m"

    if inline:
        print(prefix + message + suffix, end="", flush=True)
    else:
        print(prefix + message + suffix)

def ask(prompt_type: Prompt, message: str) -> str:
    say(Color.BLUE, message, inline=True)

    if prompt_type == Prompt.PASSWORD:
        return getpass.getpass("", echo_char="*")

    return input()

def die(message: str) -> None:
    say(Color.RED, message)
    sys.exit(1)

def run(
        command: str,
        die_message: Optional[str] = None,
        check: bool = True,
        **kwargs
    ) -> Optional[CompletedProcess]:
    try:
        return _run(shlex.split(command), check=check, **kwargs)
    except CalledProcessError:
        die(die_message or f"Command '{command}' failed unexpectedly.")

def boom(start: int) -> None:
    assert start > 0

    for i in range(start, 0, -1):
        say(Color.YELLOW, str(i) + "...")
        time.sleep(1)
