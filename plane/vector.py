from dataclasses import dataclass
from typing import Union, List

from plane.number import FiniteField, ExtensionFiniteField


@dataclass
class VectorSpace:
    degree: int
    field: Union[FiniteField, ExtensionFiniteField]


@classmethod
class SubVectorSpace:
    vector_space: VectorSpace
    basis: List['Vector']


@classmethod
class Vector:
    vector_space: VectorSpace
    elements: List[Union[FiniteField, ExtensionFiniteField]]
