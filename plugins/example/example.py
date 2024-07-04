from core.core import puts

def some(args):
    print(args)

def expo_example(args):

    match args[2]:
        case "some":
            some(args)
        case _:
            puts(f"Plugin function not found → {args[2]}", "red")