import sys

IDENT_COMMENT_START = "# so-integ-initialization-start\n"
IDENT_COMMENT_END = "# so-integ-initialization-end\n"

INIT_CODE = """
def _so_integ():
    import sys
    _old_excepthook = sys.excepthook

    def _excepthook(typ, exc, tb):
        import urllib.parse

        if _old_excepthook:
            _old_excepthook(typ, exc, tb)

        query = "{}: {}".format(typ.__name__, exc)
        if "\\n" in query:
            query = query.split("\\n")[0]

        query = urllib.parse.quote(query)
        link = "https://stackoverflow.com/search?q={}".format(query)

        sys.stderr.write("\\nSearch on stack overflow? \\n    ")
        sys.stderr.write(link)
        sys.stderr.write("\\n\\n")
        sys.stderr.flush()

    sys.excepthook = _excepthook
_so_integ()
del _so_integ
"""


def _index(a: str, b: str):
    try:
        return a.index(b)
    except ValueError:
        return -1


def _setup(install=True, uninstall=False):
    import site
    import os

    user_site = site.getusersitepackages()

    if user_site is None:
        print("user site not enabled, cannot install")
        return

    if not os.path.exists(user_site):
        os.mkdir(user_site)

    usercustomize = os.path.join(user_site, "usercustomize.py")
    if not os.path.exists(usercustomize):
        with open(usercustomize, "w"):
            pass

    with open(usercustomize, "r") as f:
        uc = f.read()

    modified = False

    start_index = _index(uc, IDENT_COMMENT_START)
    end_index = _index(uc, IDENT_COMMENT_END)

    if start_index != -1 and end_index != -1:
        have_installed = True
    elif start_index != -1 or end_index != -1 or start_index < end_index:
        raise ValueError(
            "invalid usercustomize.py installation, something is vey wrong"
        )
    else:
        have_installed = False

    if uninstall:
        if not have_installed and not install:
            print("not installed, or guard comments modified")
        uc = uc[:start_index] + uc[end_index + len(IDENT_COMMENT_END) :]
        modified = True
        have_installed = False

    if install:
        if not have_installed:
            uc += IDENT_COMMENT_START
            uc += INIT_CODE
            uc += IDENT_COMMENT_END
            modified = True
        else:
            print("already installed, use `reinstall` to reinstall")

    if modified:
        with open(usercustomize, "w") as f:
            f.write(uc)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("usage: ", sys.argv[0], "install|uninstall|reinstall")
    else:
        if sys.argv[1] == "install":
            _setup()
        elif sys.argv[1] == "uninstall":
            _setup(install=False, uninstall=True)
        elif sys.argv[1] == "reinstall":
            _setup(install=True, uninstall=True)
        else:
            print("usage: ", sys.argv[0], "install|uninstall|reinstall")
