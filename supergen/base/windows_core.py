# -*- coding: utf-8 -*-
#
# Copyright (C) 2019 Marcos Nieto Doncel
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
#     Marcos Nieto Doncel
#
import platform
import time
if platform.system() == 'Windows':
    import win32file


from supergen.base.core import Core


class WindowsCore(Core):

    def get_drive_list(self):
        drive_list = []
        drivebits = win32file.GetLogicalDrives()
        for d in range(1, 26):
            mask = 1 << d
            if drivebits & mask:
                drname = '%c:\\' % chr(ord('A') + d)
                t = win32file.GetDriveType(drname)                
                if t == win32file.DRIVE_REMOVABLE:
                    drive_list.append(drname)                 
        return drive_list
    
    def listen(self):
        while True:
            original = set(self.get_drive_list())
            #print ('Detecting...')
            time.sleep(3)
            add_device =  set(self.get_drive_list())- original
            subt_device = original - set(self.get_drive_list())

            if (len(add_device)):
                # Detected
                drive = add_device.pop()                                
                return drive
        