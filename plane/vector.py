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

    def _build_one_dim(self, a, b, c):
        return SubVectorSpace(
            self.vector_space,
            basis=[Vector(self.vector_space, [a, b, c])]
        )

    def get_line_list(self):
        one = self.field.one
        for num1 in self.field.nonzero_element():
            for num2 in self.field.nonzero_element():
                yield self._build_one_dim(one, num1, num2)
