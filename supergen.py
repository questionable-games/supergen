#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Alberto Pérez García-Plaza
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Alberto Pérez García-Plaza <alpgarcia@gmail.com>
#
import glob
import platform
import subprocess
import sys

import yaml

from supergen.util.console import Console


SNES_EXTENSIONS = ['smc', 'sfc']

DISKUTIL = ['/usr/sbin/diskutil', 'activity']

# TODO make this a singleton usable from any project file
console = Console()


def load_config(config="config.yml"):
    with open(config, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)

    emus = {'snes': cfg.get('snes'),
            'genesis': cfg.get('genesis')}

    return emus


def roms_search(mountpoint, emus):
    # Look for ROMs in the partition
    snes_roms = []
    for ext in SNES_EXTENSIONS:
        snes_pattern = mountpoint + '/**/*.' + ext
        snes_roms.extend([fname for fname in glob.glob(snes_pattern, recursive=True)])

    if len(snes_roms) > 0:
        launch_snes(emus, snes_roms)

    else:
        console.println('No roms found in {0}'.format(mountpoint))


def launch_snes(emus, snes_roms):
    if emus.get('snes'):
        console.println('Launching {0}'.format(snes_roms[0]))
        console.println('Exiting emulator with status {0}'.format(launch_game(emus['snes']['emulator'],
                                                                              emus['snes']['params'],
                                                                              snes_roms[0])))
    else:
        console.println('No emulator configured for SNES.')


def launch_game(emulator, params, rom):
    return subprocess.call([emulator, *params, rom], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():

    emus = load_config()

    console.cls()
    console.print_header()
    console.print_frame()

    platform_name = platform.system()
    console.println('Running on ' + platform_name)

    while True:
        if platform_name == 'Darwin':
            from supergen.usb import usb_osx
            mountpoint = usb_osx.listen()

        elif platform_name == 'Linux':
            from supergen.usb import usb_linux
            mountpoint = usb_linux.listen(console)

        else:
            console.println('Unsupported platform...exiting')
            sys.exit(0)

        console.println('Searching for ROMs in {0}'.format(mountpoint))
        roms_search(mountpoint, emus)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        s = "\n\nReceived Ctrl-C or other break signal. Exiting.\n"
        sys.stdout.write(s)
        sys.exit(0)
    except RuntimeError as e:
        s = "Error: %s\n" % str(e)
        sys.stderr.write(s)
        sys.exit(1)
