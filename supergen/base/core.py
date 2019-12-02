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
import subprocess

from abc import ABC, abstractmethod

import yaml


class Core(ABC):

    SNES_EXTENSIONS = ['smc', 'sfc']

    def __init__(self, console, config="config.yml"):
        self._console = console

        with open(config, 'r') as ymlfile:
            cfg = yaml.safe_load(ymlfile)

        self.__emus = {'snes': cfg.get('snes'),
                       'genesis': cfg.get('genesis')}

    @abstractmethod
    def listen(self):
        pass

    def roms_search(self, mountpoint):
        # Look for ROMs in the partition
        snes_roms = []
        for ext in self.SNES_EXTENSIONS:
            snes_pattern = mountpoint + '/**/*.' + ext
            snes_roms.extend([fname for fname in glob.glob(snes_pattern, recursive=True)])

        if len(snes_roms) > 0:
            self.launch_snes(snes_roms)

        else:
            self._console.println('No roms found in {0}'.format(mountpoint))

    def launch_snes(self, snes_roms):
        if self.__emus.get('snes'):
            self._console.println('Exiting emulator with status {0}'.format(
                self.launch_game(self.__emus['snes']['emulator'],
                                 self.__emus['snes']['params'],
                                 snes_roms[0])))
        else:
            self._console.println('No emulator configured for SNES.')

    def launch_game(self, emulator, params, rom):
        self._console.println('Launching {0}'.format(rom))
        command = [emulator]
        if params:
            command.extend(params)
        command.append(rom)
        return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def start(self):

        while True:

            mountpoint = self.listen()

            self._console.println('Searching for ROMs in {0}'.format(mountpoint))
            self.roms_search(mountpoint)