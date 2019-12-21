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
import platform
import sys


from supergen.util.console import Console


def main():

    console = Console()

    console.cls()
    console.print_header()
    console.print_frame()

    platform_name = platform.system()
    console.println('Running on {0}'.format(platform_name))

    if platform_name == 'Darwin':
        from supergen.base.osx_core import OsxCore
        core = OsxCore(console)

    elif platform_name == 'Linux':
        from supergen.base.linux_core import LinuxCore
        core = LinuxCore(console)
     
    elif platform_name == 'Windows':
        from supergen.base.windows_core import WindowsCore
        core = WindowsCore(console)        

    else:
        console.println('Unsupported platform...exiting')
        sys.exit(0)

    core.start()


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
