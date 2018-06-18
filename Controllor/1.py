import os
from pprint import pprint


def npbk():
    L = []
    for root, dirs, files in os.walk('C:\\Nox\\backup'):
        for file in files:
            if os.path.splitext(file)[1] == '.npbk':
                p = os.path.splitext(file)[0]
                L.append(p[4:])
        return L


if __name__ == "__main__":
    pprint(npbk())
