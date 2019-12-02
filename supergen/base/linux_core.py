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
import pyudev
import psutil

from time import sleep

from supergen.base.core import Core


class LinuxCore(Core):

    def listen(self):
        context = pyudev.Context()
        monitor = pyudev.Monitor.from_netlink(context)
        monitor.filter_by('block')
        # monitor.filter_by(subsystem='base')
        for device in iter(monitor.poll, None):

            if 'ID_FS_TYPE' in device:
                # print('{0} partition {1}'.format(device.action, device.get('ID_FS_LABEL')))
                self._console.println(
                    'Action: {0.action} partition {1} on {0.device_node}'.format(device, device.get('ID_FS_LABEL')))
                if device.action == 'add' and device.get('ID_FS_LABEL'):
                    # Wait until the partition corresponding to the action above is mounted
                    mountpoint = ''
                    while not mountpoint:
                        sleep(3)
                        partition_devices = {p.device: p.mountpoint for p in psutil.disk_partitions()}
                        if device.device_node in partition_devices.keys():
                            mountpoint = partition_devices[device.device_node]

                    return mountpoint

                    # print('Partition mounted  {0}: {1}'.format(device.device_node, mountpoint))
