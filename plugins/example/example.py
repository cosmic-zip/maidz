def some(args):
    print(args)

def expo(args):

    match args[1]:
        case "some":
            some(args)
        case _:
            print("Not found")