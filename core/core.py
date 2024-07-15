import json
import os
import sys
import time
import re
import subprocess
import logging
from datetime import datetime


def import_bank():
    try:
        with open("data/assets/bank.json", "r") as bank:
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
    for line in text.split("\n"):
        while len(line) > width:
            wrapped_lines.append(line[:width])
            line = line[width:]
        wrapped_lines.append(line)
    return "\n".join(wrapped_lines)


def logfile(command: dict):

    log = {
        "name": command["name"],
        "origin": command["command"],
        "output": command["output"],
        "datetime": str(datetime.now()),
    }

    with open("data/output/maid_exec_doc.jsonl", "a") as f:
        parsed = json.dumps(log, sort_keys=True)
        f.write(f"{parsed}\n")
        f.close()


def exec(command):
    try:
        if not command:
            exit()

        log = {}
        puts(command["name"], "purple")
        result = subprocess.run(
            command["command"], shell=True, capture_output=True, text=True
        )

        if result.returncode == 0:
            output = result.stdout
            command["output"] = wrap(output)
            logfile(command)
            print(command["output"])
        else:
            puts(f"Error: {result.stderr}", "red")
    except Exception as err:
        puts(f"Command not found in bank.json :: {err} :: ", "orange")


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


def exec_batch(chunk: dict, args: list, delay=None):

    for q in chunk:
        args[1] = q["name"]
        out = query([q], args)
        exec(out)
        if delay:
            time.sleep(delay)

    return 0