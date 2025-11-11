#! /usr/bin/env python

from bais.base import Base
from bais.chroot import Chroot

def main() -> None:
    Base().run()
    Chroot().run()
