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

from collections import deque
from datetime import datetime

import colorama


class Console:

    __SUPER_COLOR = colorama.Style.BRIGHT + colorama.Fore.RED
    __GEN_COLOR = colorama.Style.BRIGHT + colorama.Fore.BLUE

    __lines = deque(maxlen=5)
    __max_len = 0

    def __init__(self):
        colorama.init(autoreset=True)

    def __move_cursor(self, x, y):
        print ("\x1b[{};{}H".format(y, x))

    def cls(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_header(self):
        print(self.__SUPER_COLOR + "     __ __     _____                       " +
              self.__GEN_COLOR + "______                __ __ ")
        print(self.__SUPER_COLOR + "  __/ // /_   / ___/__  ______  ___  _____" +
              self.__GEN_COLOR + "/ ____/__  ____     __/ // /_")
        print(self.__SUPER_COLOR + r" /_  _  __/   \__ \/ / / / __ \/ _ \/ ___/" +
              self.__GEN_COLOR + r" / __/ _ \/ __ \   /_  _  __/")
        print(self.__SUPER_COLOR + "/_  _  __/   ___/ / /_/ / /_/ /  __/ /  " +
              self.__GEN_COLOR + "/ /_/ /  __/ / / /  /_  _  __/ ")
        print(self.__SUPER_COLOR + r" /_//_/     /____/\__,_/ .___/\___/_/   " +
              self.__GEN_COLOR + r"\____/\___/_/ /_/    /_//_/    ")
        print(self.__SUPER_COLOR + "                      /_/                                              ")

    def print_frame(self):
        self.__move_cursor(1, 7)
        print('-----')
        self.__move_cursor(1, 13)
        print('-----')

    def println(self, message):
        message = str(message)

        self.__lines.append(message)
        if len(message) + 33 > self.__max_len:
            self.__max_len = len(message) + 33

        y = 8
        for line in self.__lines:
            if len(self.__lines) == (y - 7):
                prompt = '-> ' + colorama.Style.BRIGHT + colorama.Fore.GREEN + '[SuperGen]'
            else:
                prompt = colorama.Style.RESET_ALL + '|  [SuperGen]'

            self.__move_cursor(1, y)
            blank_line = ' '
            for i in range(self.__max_len):
                blank_line += ' '
            print(blank_line, end='\r')
            print(prompt +
                  colorama.Style.RESET_ALL + ' [' + datetime.now().strftime('%d-%m-%y %H:%M:%S') + '] ' +
                  line)
            y += 1
