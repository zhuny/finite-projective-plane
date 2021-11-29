from plane.number import FiniteField
from plane.projective import construct


def run():
    construct(FiniteField(7))


if __name__ == '__main__':
    run()
