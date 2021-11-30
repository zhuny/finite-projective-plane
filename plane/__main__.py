import sys
from pathlib import Path

from plane.number import FiniteField
from plane.projective import construct
from plane.util import is_prime


def run():
    if len(sys.argv) <= 1:
        print(sys.argv[0], "{info.txt}")
        return

    with Path(sys.argv[1]).open(encoding='utf8') as f:
        # Get degree of finite projective plane
        n = f.readline().strip()
        if not n.isdigit():
            print("First line should be a number.")
            return

        n = int(n)
        if not is_prime(n):
            print("Degree should be a prime number")
            return

        # load element
        elements = set()
        for line in f:
            elements.update(line.split())

        if len(elements) < n*n + n + 1:
            print("The number of elements should be "
                  "greater than or equal to 'n*n+n+1'")
            return

        structure = construct(FiniteField(n), list(elements))
        for g in structure:
            print(",".join(g))


if __name__ == '__main__':
    run()
