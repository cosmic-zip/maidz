from plugins import example.expo


def expo(args: list):

    match args[1]:
        case "example":
            example.expo(args)
        case _:
            print("Not found")
