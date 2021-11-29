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

    def is_orthogonal(self, other: 'SubVectorSpace'):
        for base1 in self.basis:
            for base2 in other.basis:
                if not base1.is_orthogonal(base2):
                    return False
        return True


@dataclass
class Vector:
    vector_space: VectorSpace
    elements: List[Field]

    def is_orthogonal(self, other: 'Vector'):
        total_sum = self.vector_space.field.zero
        for x, y in zip(self.elements, other.elements):
            total_sum += x*y
        return total_sum.is_zero()


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

    def get_point_list(self):
        one = self.field.one
        for num1 in self.field.nonzero_element():
            for num2 in self.field.nonzero_element():
                yield self._build_one_dim(one, num1, num2)
