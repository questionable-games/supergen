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
import subprocess
import sys
import unittest

from mock import patch, MagicMock

# Make sure we use our code and not any other could we have installed
sys.path.insert(0, '..')

from supergen.base.linux_core import LinuxCore
from supergen.base.osx_core import OsxCore


class TestCore(unittest.TestCase):

    def test_launch_game_with_no_params(self):
        """Test launch game calls `subprocess.call` with the no emulator params"""

        # Mock console instance
        with patch('supergen.util.console.Console') as mock:
            console = mock.return_value

            # Create the real objects to test based on the mocked console and a dummy config file
            osx_core = OsxCore(console=console, config='dummy_config.yml')

            # Mock `subprocess.call` method, we will
            subprocess.call = MagicMock(return_value=1)

            # Test case: params are `None`
            result = osx_core.launch_game('emu', None, 'rom')
            subprocess.call.assert_called_once_with(['emu', 'rom'],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
            # Check the method returns the return value coming from the mocked method
            assert result == 1

            # Same test for `linux_core` (should be the same method from `Core` class)
            linux_core = LinuxCore(console=console, config='dummy_config.yml')
            subprocess.call = MagicMock(return_value=0)
            result = linux_core.launch_game('emu', None, 'rom')
            subprocess.call.assert_called_once_with(['emu', 'rom'],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
            assert result == 0

    def test_launch_game_with_empty_params_list(self):
        """Test launch game calls `subprocess.call` with the an empty list as emulator params"""

        # Mock console instance
        with patch('supergen.util.console.Console') as mock:
            console = mock.return_value

            # Create the real objects to test based on the mocked console and a dummy config file
            osx_core = OsxCore(console=console, config='dummy_config.yml')

            # Mock `subprocess.call` method, we will
            subprocess.call = MagicMock(return_value=1)

            # Test case: params are `None`
            result = osx_core.launch_game('emu', [], 'rom')
            subprocess.call.assert_called_once_with(['emu', 'rom'],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
            # Check the method returns the return value coming from the mocked method
            assert result == 1

            # Same test for `linux_core` (should be the same method from `Core` class)
            linux_core = LinuxCore(console=console, config='dummy_config.yml')
            subprocess.call = MagicMock(return_value=2)
            result = linux_core.launch_game('emu', [], 'rom')
            subprocess.call.assert_called_once_with(['emu', 'rom'],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
            assert result == 2

    def test_launch_game_with_params_list(self):
        """Test launch game calls `subprocess.call` with the a list as emulator params"""

        # Mock console instance
        with patch('supergen.util.console.Console') as mock:
            console = mock.return_value

            # Create the real objects to test based on the mocked console and a dummy config file
            osx_core = OsxCore(console=console, config='dummy_config.yml')

            # Mock `subprocess.call` method, we will
            subprocess.call = MagicMock(return_value=5)

            # Test case: params are `None`
            result = osx_core.launch_game('emu', ['-p', 'param'], 'rom')
            subprocess.call.assert_called_once_with(['emu', '-p', 'param', 'rom'],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
            # Check the method returns the return value coming from the mocked method
            assert result == 5

            # Same test for `linux_core` (should be the same method from `Core` class)
            linux_core = LinuxCore(console=console, config='dummy_config.yml')
            subprocess.call = MagicMock(return_value=3)
            result = linux_core.launch_game('emu', ['-p', 'param'], 'rom')
            subprocess.call.assert_called_once_with(['emu', '-p', 'param', 'rom'],
                                                    stdout=subprocess.DEVNULL,
                                                    stderr=subprocess.DEVNULL)
            assert result == 3
