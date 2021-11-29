import dataclasses
from dataclasses import dataclass
from typing import List

from plane.number import Field


@dataclass
class VectorSpace:
    degree: int
    field: Field


@dataclass
class SubVectorSpace:
    vector_space: VectorSpace
    basis: List['Vector']


@dataclass
class Vector:
    vector_space: VectorSpace
    elements: List[Field]


@dataclass
class ProjectivePlane:
    field: Field
    vector_space: VectorSpace = dataclasses.field(init=False)

    def __post_init__(self):
        self.vector_space = VectorSpace(3, self.field)
