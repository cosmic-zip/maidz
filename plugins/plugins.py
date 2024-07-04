from plugins.example.example import expo_example
from core.core import puts


def expo(args: list):

    if len(args) < 4:
        puts("Bad expo call :: Use expo plugin_name --key value", "red")
        exit()

    # drop expo name
    # expo plugin_name --key value
    args.pop(1)

    match args[1]:
        case "example":
            expo_example(args)
        case _:
            puts(f"Plugin not found → {args[1]}", "red")
