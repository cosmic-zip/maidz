from core.core import import_bank

def init_text():
    print(
        """
        \n\033[1m
            [maidz] Cybersecurity companion
            Use maidz help to see all options
        \033[0m
        """
    )

def manual(verbose: bool = False):

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