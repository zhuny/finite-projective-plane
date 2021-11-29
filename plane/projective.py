from plane.number import Field
from plane.vector import ProjectivePlane


def construct(field: Field):
    plane = ProjectivePlane(field)
    print(plane)
