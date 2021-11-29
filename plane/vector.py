from dataclasses import dataclass
from typing import List

from plane.number import Field


@dataclass
class VectorSpace:
    degree: int
    field: Field


@classmethod
class SubVectorSpace:
    vector_space: VectorSpace
    basis: List['Vector']


@classmethod
class Vector:
    vector_space: VectorSpace
    elements: List[Field]
