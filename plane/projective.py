import random

from plane.number import Field
from plane.vector import ProjectivePlane


def construct(field: Field, elements):
    plane = ProjectivePlane(field)
    line_list = list(plane.get_point_list())
    random.shuffle(line_list)
    pair_list = list(zip(line_list, elements))

    assert len(line_list) == len(pair_list)

    for normal in line_list:
        plane_element = [
            element
            for line, element in pair_list
            if line.is_orthogonal(normal)
        ]
        print(plane_element)
    print(len(line_list))
