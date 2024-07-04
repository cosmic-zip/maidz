#!/usr/bin/env python3
# -----------------------------------------------------------------------------#
#   MaidZ Cybersecurity Companion                                              #
#   Copyright (C) 2024  cosmic-zip                                             #
#                                                                              #
#                                                                              #
#   This program is free software: you can redistribute it and/or modify       #
#   it under the terms of the GNU Affero General Public License as published   #
#   by the Free Software Foundation, either version 3 of the License, or       #
#   (at your option) any later version.                                        #
#                                                                              #
#   This program is distributed in the hope that it will be useful,            #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#   GNU Affero General Public License for more details.                        #
#                                                                              #
#   You should have received a copy of the GNU Affero General Public License   #
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
# -----------------------------------------------------------------------------#


import sys

from core.mtop import mtop
from core.core import *
from core.server import mint_server
from core.extras import *


def shell(args):

    if len(args) < 2:
        init_text()

    DATA_BANK = import_bank()

    match args[1]:
        case "manual":
            manual(true)
        case "mtop":
            mtop()
        case "mitm.server":
            mint_server(args)
        case "map.dns":
            exec_batch(DATA_BANK["dns"], args)
        case _:
            q = query(DATA_BANK["general"], args)
            return exec(q)

    return 0


if __name__ == "__main__":
    try:
        shell(sys.argv)
    except Exception as err:
        puts(str(err), "red")
