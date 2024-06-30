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


import json, os, sys, time, re, subprocess, platform

def banner():
    os.system("chafa apron/assets/sakuya_izayoi.png")
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
        with open("apron/assets/bank.json", "r") as bank:
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

def wrap(text, width=160):
    wrapped_lines = []
    for line in text.split('\n'):
        while len(line) > width:
            wrapped_lines.append(line[:width])
            line = line[width:]
        wrapped_lines.append(line)
    return '\n'.join(wrapped_lines)

def exec(command):
    try:
        puts(command["name"], "purple")
        result = subprocess.run(command["command"], shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            output = result.stdout
            wrapped_output = wrap(output)
            print(wrapped_output)
        else:
            puts(f"Error: {result.stderr}", "red")
    except Exception as err:
        puts(str(err), "red")

def key_value(term: str, args: list):

    if len(args) < 1:
        print("Args are to small")

    for index, item in enumerate(args):
        if item == term:
            if index + 1 >= len(args):
                puts("Incomplete key-value constrain :: return empty")
                return ""
            # print(args[index +1])
            return args[index + 1]

    puts(f"No value found for key: {term} :: return empty")
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
        puts(f"Command not found for {args[1]}", "red")
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

def get_ram_usage():
    with open('/proc/meminfo', 'r') as f:
        lines = f.readlines()
    mem_total = int(lines[0].split()[1])
    mem_free = int(lines[1].split()[1])
    mem_available = int(lines[2].split()[1])
    return mem_total, mem_free, mem_available

def get_desktop_environment():
    desktop_session = os.environ.get('DESKTOP_SESSION')
    if desktop_session:
        if desktop_session == 'ubuntu':
            return 'GNOME'
        return desktop_session
    elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):
        return 'GNOME'
    elif os.environ.get('KDE_FULL_SESSION'):
        return 'KDE'
    elif os.environ.get('XDG_CURRENT_DESKTOP'):
        return os.environ.get('XDG_CURRENT_DESKTOP')
    else:
        return 'Unknown'


def neolain():

    with open('/proc/loadavg', 'r') as f:
        load_avg = f.readline().strip().split()[:3]
    cpu_load = tuple(float(x) for x in load_avg)

    mem_total, mem_free, mem_available = get_ram_usage()
    os_name = platform.system()
    kernel_version = platform.release()
    shell = os.environ.get('SHELL')
    desktop_environment = get_desktop_environment()

    var = f"""
    
         |\\---/|
         | ,_, |
          \\_`_/-..----.
         ___/ `   ' ,""+ \\  MaidZ
        (__...'   __\\    |`.___.';
          (_,...'(_,.`__)/'.....+

        {f"⬥ CPU:{cpu_load[1]}"}
        {f"⬥ Total RAM: {int(mem_total/1024)} MB"}
        {f"⬥ Free RAM: {int(mem_free/1024)} MB"}
        {f"⬥ Available RAM: {int(mem_available/1024)} MB"}
        {f"⬥ OS Name: {os_name}"}
        {f"⬥ Kernel Version: {kernel_version}"}
        {f"⬥ Shell: {shell}"}
        {f"⬥ Desktop Environment: {desktop_environment}"}

        ☺  ☻  ♥  ♦  ♣  ♠  •  ◘
        ○  ◙  ♂  ♀  ♪  ♫  ☼  ►
        ◄  ↕  ‼  ¶  §  ▬  ↨  ↑
        ↓  →  ←  ∟  ↔  ▲  ▼  *
    
    """

    puts(var)


def mint(args):
    pass


def shell(args):

    if len(args) < 2:
        banner()
        return 255

    if args[1] == "help":
        verbose = False
        for x in args:
            if x == "-v":
                verbose = True
        help(verbose)
    elif args[1] == "banner":
        banner()
    elif args[1] == "status":
        neolain()
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
    try:
        shell(sys.argv)
    except KeyboardInterrupt:
        pass
