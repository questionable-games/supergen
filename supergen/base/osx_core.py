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
import os

from time import sleep
from subprocess import Popen, PIPE

from supergen.base.core import Core


class OsxCore(Core):

    DISKUTIL = ['/usr/sbin/diskutil', 'activity']

    def listen(self):
        with Popen(self.DISKUTIL, stdout=PIPE, encoding='UTF-8') as diskutil:
            # Ignore events that describe the present state
            for line in diskutil.stdout:
                # print(line)
                if line.startswith('***DAIdle'):
                    break

            # Detect the first subsequent "Disk Appeared" event
            for line in diskutil.stdout:
                # print(line)
                if line.startswith('***DiskMountApproval'):
                    # print(line)
                    # e.g. ***DiskAppeared ('disk2s1', DAVolumePath = '<null>', DAVolumeKind = 'msdos', DAVolumeName = 'EMTEC8') Time=20191113-00:03:19.0797
                    volume_name = line[line.find('DAVolumeName '):line.find('\')')]
                    volume_name = volume_name[volume_name.find('\'') + 1:]
                    mountpoint = '/Volumes/' + volume_name
                    break

        # Wait until disk is mounted
        while not os.path.ismount(mountpoint):
            sleep(3)
        return mountpoint
