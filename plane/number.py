from dataclasses import dataclass
from typing import List, Union


@dataclass
class FiniteField:
    order: int  # prime number


@dataclass
class FiniteFieldElement:
    # Element of Finite Field
    number: int
    finite_field: FiniteField


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
