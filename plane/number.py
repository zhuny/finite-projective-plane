from dataclasses import dataclass
from typing import List, Union


@dataclass
class FiniteField:
    order: int  # prime number

    @property
    def one(self):
        return FiniteFieldElement(1, self)

    @property
    def zero(self):
        return FiniteFieldElement(0, self)

    def nonzero_element(self):
        for i in range(1, self.order):
            yield FiniteFieldElement(i, self)


@dataclass
class FiniteFieldElement:
    # Element of Finite Field
    number: int
    finite_field: FiniteField

    def __post_init__(self):
        self.number %= self.finite_field.order

    def __mul__(self, other: 'FiniteFieldElement'):
        return FiniteFieldElement(
            self.number * other.number,
            self.finite_field
        )

    def __add__(self, other: 'FiniteFieldElement'):
        return FiniteFieldElement(
            self.number + other.number,
            self.finite_field
        )

    def is_zero(self):
        return self.number == 0


@dataclass
class ExtensionFiniteField:
    finite_field: FiniteField
    degree: int  # >= 2


@dataclass
class ExtensionFiniteFieldElement:
    # Element of Extension Finite Field
    extension_finite_field: ExtensionFiniteField
    numbers: List[FiniteFieldElement]


Field = Union[FiniteField, ExtensionFiniteField]  # 사칙연산이 가능한 수 쳬계
