#!/usr/bin/env python3
# -----------------------------------------------------------------------------#
#   MaidZ Cybersecurity companion                                              #
#   Copyright (C) 2024  Prism-zip                                              #
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


import json, os, sys, time, re

import subprocess

def wrap(text, width=160):
    wrapped_lines = []
    for line in text.split('\n'):
        while len(line) > width:
            wrapped_lines.append(line[:width])
            line = line[width:]
        wrapped_lines.append(line)
    return '\n'.join(wrapped_lines)

def exec(command):
    puts(command["name"])
    result = subprocess.run(command["command"], shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        output = result.stdout
        wrapped_output = wrap(output)
        print(wrapped_output)
    else:
        puts(f"[error] :: {result.stderr}", "red")


def sakuya():
    os.system("chafa -s 90x90 assets/sakuya_izayoi.png")
    print(
        """
        \n\033[1m
            [maidz] Cybersecurity companion
            Use maidz help to see all options
        \033[0m
        """
    )


def import_bank():
    try:
        with open("bank.json", "r") as bank:
            return json.load(bank)
    except json.JSONDecodeError as e:
        print(f"JSON::ERROR {e}")


def puts(string: str, color: str = ""):
    color_emojis = {
        "purple": "🟣",
        "red": "🔴",
        "green": "🟢",
        "yellow": "🟡",
        "blue": "🔵",
        "orange": "🟠",
        "white": "⚪",
        "black": "⚫",
    }
    emoji = ""
    if color != "":
        emoji = color_emojis.get(color)
    print(f"\033[1m{emoji} {string}\033[0m")


def key_value(term: str, args: list):

    if len(args) < 1:
        print("args are to small")

    for index, item in enumerate(args):
        if item == term:
            if index + 1 >= len(args):
                puts("Incomplete key-value constrain :: return empty")
                return ""
            # print(args[index +1])
            return args[index + 1]

    puts(f"no value found for key: {term} :: return empty")
    return ""


def query(data: dict, args: list):

    name = ""
    content = ""
    description = ""
    pattern = r"\s*@@(\w+)\s*"

    for ctn in data:
        if ctn["name"] == args[1]:
            content = ctn["command"]
            name = ctn["name"]
            description = ctn["description"]

    if not content:
        puts(f"bind not found for {args[1]}")
        return None

    matches = re.findall(pattern, content)
    for match in matches:
        key = match.strip()
        value = key_value(f"--{key}", args)
        content = content.replace(f"@@{key}", value)

    # print(content)
    return {"name": name, "command": content, "description": description}


def exec_batch(chunk: dict, args: list, delay = None):

    for q in chunk:
        out = query(chunk, args)
        if delay:
            time.sleep(delay)
        print(out)


def help(verbose: bool = False):

    data = import_bank()
    data = data["general"]

    for d in data:
        puts(d["name"], "yellow")
        puts(f"\n\t{d['description']}")
        if verbose:
            print(f"\n\t{d['command']}\n")
        print("")


def install_deps():
    deps = import_bank()
    deps = deps["deps"]
    for pkg in deps:
        puts(f"PKG :: {pkg}")
        os.system(f"sudo apt install {pkg} -y")


def shell(args):

    if len(args) < 2:
        sakuya()
        return 255

    if args[1] == "help":
        verbose = False
        for x in args:
            if x == "-v":
                verbose = True
        help(verbose)
    elif args[1] == "sakuya":
        sakuya()
    elif args[1] == "install":
        install_deps()
    elif args[1] == "query":
        data = import_bank()
        query(data["general"], args)
    else:
        data = import_bank()
        out = exec(query(data["general"], args))
        return out

    return 0


if __name__ == "__main__":
    shell(sys.argv)
