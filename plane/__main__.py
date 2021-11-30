import sys
from pathlib import Path

from plane.number import FiniteField
from plane.projective import construct


def run():
    if len(sys.argv) <= 1:
        print(sys.argv[0], "{info.txt}")
        return

    with Path(sys.argv[1]).open(encoding='utf8') as f:
        n = f.readline().strip()
        if not n.isdigit():
            print("First line should be a prime number.")
            return

        n = int(n)
        elements = set()

        for line in f:
            elements.update(line.split())

        structure = construct(
            FiniteField(n),
            elements
        )
        for g in structure:
            print(",".join(g))


if __name__ == '__main__':
    run()
