import json, os, sys, time, re


def import_bank():
    try:
        with open("bank.json", "r") as bank:
            return json.load(bank)
    except json.JSONDecodeError as e:
        print(f"JSON::ERROR {e}")

def puts(string: str):
    print(f"\033[1m🟣 {string}\033[0m")

def key_value(term: str, args: list):


    if len(args) < 1:
        print("args are to small")
        
    for index, item in enumerate(args):
        if item == term:
            if index + 1 >= len(args):
                puts("Incomplete key-value constrain :: return empty")
                return ""
            print(args[index +1])
            return args[index +1]

    puts(f"no value found for key: {term} :: return empty")
    return ""
    
    
def query(data: dict, args: list):
    
    pattern = r'\s*@@(\w+)\s*'
    
    content = None
    for ctn in data:
        if ctn["name"] == args[1]:
            content = ctn["command"]
    
    if not content:
        puts(f"bind not found for {args[1]}")
    
    
    matches = re.findall(pattern, content)
    for match in matches:
        key = match.strip()
        value = key_value(f"--{key}", args)
        content = content.replace(f'@@{key}', value)
    
    print(content)
    return content
    
def exec(args: list):
    pass

def exec_batch(chunk: dict, args: list, delay: int = 0):

    for q in chunk:
        out = query(chunk, args)
        if delay:
            time.sleep(delay)
        print(out)

def manual():

    data = import_bank()
    data = data["general"]

    for d in data:
        puts(d['name'])
        puts(d['description'])
        print(f"\n\t{d['command']}\n")

if __name__ == '__main__':

    manual()
